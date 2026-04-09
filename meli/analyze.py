# -*- coding: utf-8 -*-
"""
MercaFlow — Product Analysis via Claude
Takes product images → outputs all listing content in one call.
"""
import sys
import io
import os
import json
import base64
import requests
from pathlib import Path
from dotenv import load_dotenv

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ENV_PATH = Path(__file__).parent.parent / ".env"
load_dotenv(ENV_PATH)


def get_claude_key():
    return os.environ.get("ANTHROPIC_OAUTH_KEY", "")


def encode_image(path):
    """Read image file and return base64 + mime type (auto-detected from magic bytes)."""
    with open(path, 'rb') as f:
        data = f.read()
    
    # Detect actual format from magic bytes (file extension can lie)
    if data[:8] == b'\x89PNG\r\n\x1a\n':
        mime = 'image/png'
    elif data[:2] == b'\xff\xd8':
        mime = 'image/jpeg'
    elif data[:4] == b'RIFF' and data[8:12] == b'WEBP':
        mime = 'image/webp'
    elif data[:6] in (b'GIF87a', b'GIF89a'):
        mime = 'image/gif'
    else:
        # Fallback to extension
        ext = Path(path).suffix.lower()
        mime = {'.png': 'image/png', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.webp': 'image/webp'}.get(ext, 'image/png')
    
    return base64.b64encode(data).decode(), mime


def pick_best_category(image_paths, product_name, candidates):
    """
    Ask Claude to pick the best-fitting category from a list of domain_discovery candidates.

    Args:
        image_paths: list of image file paths (same set used by analyze_product)
        product_name: the Spanish product name that produced these candidates
        candidates: list of dicts from /domain_discovery/search; each has at least
                    'category_id' and 'category_name'

    Returns:
        category_id string of the best match. Falls back to candidates[0]['category_id']
        if Claude's response can't be parsed or doesn't match any candidate.
    """
    if not candidates:
        raise ValueError("pick_best_category: no candidates provided")
    if len(candidates) == 1:
        return candidates[0]['category_id']

    # Build the candidate list for Claude
    lines = []
    for i, c in enumerate(candidates, 1):
        cid = c.get('category_id', '?')
        name = c.get('category_name', '?')
        lines.append(f"{i}. {cid} — {name}")

    prompt = f"""Look at the product images. The product name is: "{product_name}"

MercadoLibre returned these candidate categories:
{chr(10).join(lines)}

Pick the SINGLE best-fitting category for the product visible in the images.
Return ONLY the category_id (e.g. "MLM168251") with no other text, explanation, or punctuation."""

    content = [{"type": "text", "text": "Product images:"}]
    for img_path in image_paths:
        b64, mime = encode_image(img_path)
        content.append({
            "type": "image",
            "source": {"type": "base64", "media_type": mime, "data": b64}
        })
    content.append({"type": "text", "text": prompt})

    key = get_claude_key()
    resp = requests.post('https://api.anthropic.com/v1/messages',
        headers={
            'anthropic-version': '2023-06-01',
            'anthropic-beta': 'claude-code-20250219,oauth-2025-04-20',
            'Authorization': f'Bearer {key}',
            'Content-Type': 'application/json',
        },
        json={
            'model': 'claude-sonnet-4-20250514',
            'max_tokens': 50,
            'system': [{'type': 'text', 'text': "You are Claude Code, Anthropic's official CLI for Claude."}],
            'messages': [{'role': 'user', 'content': content}]
        },
        timeout=60
    )

    if resp.status_code != 200:
        # Fall back rather than break the pipeline
        return candidates[0]['category_id']

    text = ''.join(b.get('text', '') for b in resp.json().get('content', []) if b.get('type') == 'text').strip()

    import re
    match = re.search(r'MLM\d+', text)
    if not match:
        return candidates[0]['category_id']

    chosen = match.group(0)
    if any(c.get('category_id') == chosen for c in candidates):
        return chosen
    # Claude returned a category_id that wasn't in the list — fall back
    return candidates[0]['category_id']


def analyze_product(image_paths, category_attributes=None, defaults=None, notes=None):
    """
    Analyze product images with Claude and generate all listing content.
    
    Args:
        image_paths: list of image file paths
        category_attributes: list of attribute dicts from MeLi API (optional, improves accuracy)
        defaults: dict of fixed values like {"brand": "DAJIBA"} that override Claude's guesses
        notes: extra context about the product (e.g. "3-pack", "darker than photo", "waterproof")
    
    Returns:
        dict with all listing content
    """
    defaults = defaults or {}
    
    # Build the attribute list for Claude if we have category data
    attr_instructions = ""
    if category_attributes:
        attr_list = []
        for attr in category_attributes:
            attr_id = attr.get('id', '')
            name = attr.get('name', '')
            values = attr.get('values', [])
            value_type = attr.get('value_type', 'string')
            tags = attr.get('tags', {})
            
            # Skip system/internal attributes
            skip = ['VERTICAL_TAGS', 'DESCRIPTIVE_TAGS', 'PRODUCT_DATA_SOURCE', 
                    'SELLER_PACKAGE_DATA_SOURCE', 'PACKAGE_DATA_SOURCE', 'SYI_PYMES_ID',
                    'EXCLUDED_PLATFORMS', 'LIMITED_MARKETPLACE_VISIBILITY_REASONS',
                    'SEARCH_ENHANCEMENT_FIELDS', 'CATALOG_TITLE', 'IS_NEW_OFFER',
                    'ADDITIONAL_INFO_REQUIRED', 'EMPTY_GTIN_REASON']
            if attr_id in skip:
                continue
            
            # Skip attributes that have defaults
            if attr_id in defaults:
                continue
                
            val_options = [v.get('name', '') for v in values[:10]]
            required = tags.get('required', False)
            
            entry = f"- {attr_id} ({name})"
            if required:
                entry += " [REQUIRED]"
            if val_options:
                entry += f": options are [{', '.join(val_options)}]"
            elif value_type == 'number_unit':
                entry += ": provide number with unit (e.g. '35 cm', '600 g')"
            
            attr_list.append(entry)
        
        attr_instructions = f"""
CATEGORY ATTRIBUTES TO FILL:
Fill as many as possible based on what you can see in the images.
If you cannot determine a value, skip it. Do not guess dimensions or weight — only include if clearly visible or deducible.

{chr(10).join(attr_list)}
"""

    # Build default overrides instruction
    defaults_text = ""
    if defaults:
        defaults_text = f"""
FIXED VALUES (already set, do not include these in attributes):
{json.dumps(defaults, ensure_ascii=False, indent=2)}
"""

    # Build notes context
    notes_text = ""
    if notes:
        notes_text = f"""
IMPORTANT CONTEXT FROM SELLER (consider this when generating content):
{notes}
"""

    prompt = f"""You are analyzing product images for a MercadoLibre Mexico listing.
Look at ALL the images carefully and generate the complete listing content in Spanish.

TITLE RULES:
1. Format: [Producto] + [Marca/Modelo] + [Atributo clave] + [Material/Uso] + [Medida]
2. MUST be under 60 characters. Every word must add search value.
3. No hype words (oferta, increíble, calidad, premium, original).
4. Product type goes first (what people search for).

DESCRIPTION TEMPLATE — follow this structure exactly:

  Line 1: [Product name] + one sentence describing what it is and its main benefit.

  Section "CARACTERISTICAS PRINCIPALES:"
  - Each feature on its own line
  - Blank line between each bullet point
  - Only describe what you can SEE in the images
  - Include: material, structure, mechanism, color, text/branding visible

  Section "IDEAL PARA:"
  - 3-4 use cases (where/how to use it)
  - Blank line between each

  Section "INCLUYE:"
  - What comes in the box/package
  - Be specific (1x product, 1x frame, etc.)

  Section "ESPECIFICACIONES:"
  - Only if you can determine from images
  - Dimensions, weight, capacity if visible
  - If you cannot determine, skip this section entirely

DESCRIPTION RULES:
- Plain text only. No HTML, no emojis, no special characters.
- Use \n for line breaks and \n\n for blank lines between bullet points.
- All text in Spanish (Mexico).
- Be factual — only describe what you can actually see.
- DO NOT invent dimensions, weight, or capacity you cannot see.
- DO NOT include shipping or warranty text — that is added separately.
{notes_text}
{defaults_text}
{attr_instructions}
Return ONLY valid JSON with this exact structure:
{{
    "product_name": "short product name for category search",
    "family_name": "SEO title under 60 chars",
    "title_alternatives": ["option 2 under 60 chars", "option 3 under 60 chars"],
    "description": "full description following the template above",
    "attributes": {{
        "ATTRIBUTE_ID": "value",
        "ATTRIBUTE_ID2": "value2"
    }},
    "search_keywords": ["keyword1", "keyword2", "keyword3"]
}}"""

    # Build message with images
    content = [{"type": "text", "text": "Product images to analyze:"}]
    
    for i, img_path in enumerate(image_paths):
        b64, mime = encode_image(img_path)
        content.append({
            "type": "image",
            "source": {"type": "base64", "media_type": mime, "data": b64}
        })
    
    content.append({"type": "text", "text": prompt})

    # Call Claude
    key = get_claude_key()
    resp = requests.post('https://api.anthropic.com/v1/messages',
        headers={
            'anthropic-version': '2023-06-01',
            'anthropic-beta': 'claude-code-20250219,oauth-2025-04-20',
            'Authorization': f'Bearer {key}',
            'Content-Type': 'application/json',
        },
        json={
            'model': 'claude-sonnet-4-20250514',
            'max_tokens': 4000,
            'system': [{'type': 'text', 'text': "You are Claude Code, Anthropic's official CLI for Claude."}],
            'messages': [{'role': 'user', 'content': content}]
        },
        timeout=60
    )
    
    if resp.status_code != 200:
        raise Exception(f"Claude API error {resp.status_code}: {resp.text[:300]}")
    
    result = resp.json()
    text = ''.join(b.get('text', '') for b in result.get('content', []) if b.get('type') == 'text')
    
    # Parse JSON from response
    try:
        # Find JSON in response (Claude might wrap it in markdown)
        start = text.index('{')
        end = text.rindex('}') + 1
        data = json.loads(text[start:end])
    except (ValueError, json.JSONDecodeError) as e:
        raise Exception(f"Failed to parse Claude response: {e}\nRaw: {text[:500]}")
    
    # Merge defaults into attributes
    if defaults:
        for k, v in defaults.items():
            if k not in data.get('attributes', {}):
                data['attributes'][k] = v
    
    # Append standard footer to description
    warranty = defaults.get('WARRANTY_TIME', '30 días')
    footer = f"""\n\nENVIO:\n\nEnviamos a toda la Republica Mexicana con Mercado Envios.\n\nGARANTIA:\n\nProducto nuevo con garantia de {warranty}.\n\nSi tienes alguna duda, no dudes en preguntar."""
    
    if 'description' in data:
        data['description'] = data['description'] + footer
    
    return data


if __name__ == "__main__":
    import glob
    import time
    from meli.client import MeliClient
    
    # Test with laundry basket images
    images = sorted(glob.glob('evals/laundry-basket-test/picset-output/batch-*.png'))[:3]
    
    if not images:
        print("No test images found")
        sys.exit(1)
    
    print(f"Analyzing {len(images)} images...\n")
    
    # Get category attributes for better results
    client = MeliClient()
    
    # First find category
    results = client.get('/sites/MLM/domain_discovery/search', params={'q': 'cesto ropa sucia plegable'})
    cat_id = results[0]['category_id'] if results else 'MLM168251'
    print(f"Category: {cat_id}")
    
    # Get attributes
    attrs = client.get_category_attributes(cat_id)
    print(f"Attributes: {len(attrs)} total\n")
    
    # Defaults
    defaults = {
        "BRAND": "DAJIBA",
        "ITEM_CONDITION": "Nuevo",
        "SELLER_SKU": "DAJIBA-CESTO-001",
    }
    
    t0 = time.time()
    result = analyze_product(images, category_attributes=attrs, defaults=defaults)
    t1 = time.time()
    
    print(f"Done in {t1-t0:.1f}s\n")
    print(f"Product name: {result.get('product_name')}")
    print(f"Family name:  {result.get('family_name')} ({len(result.get('family_name', ''))} chars)")
    print(f"Keywords:     {result.get('search_keywords')}")
    print(f"\nDescription:\n{result.get('description', '')[:500]}")
    print(f"\nAttributes ({len(result.get('attributes', {}))}):")
    for k, v in result.get('attributes', {}).items():
        print(f"  {k}: {v}")
