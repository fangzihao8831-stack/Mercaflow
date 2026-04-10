# -*- coding: utf-8 -*-
"""
MercaFlow — Product Analysis
Takes product images → outputs all listing content via the configured LLM provider.
"""
import sys
import io
import json
import re

try:
    sys.stdout.reconfigure(encoding='utf-8')
except (AttributeError, ValueError):
    pass

from meli.llm import call_vision


def pick_best_category(image_paths, product_name, candidates):
    """
    Ask the LLM to pick the best-fitting MeLi category from domain_discovery candidates.

    Args:
        image_paths: list of image file paths
        product_name: the Spanish product name that produced these candidates
        candidates: list of dicts with at least 'category_id' and 'category_name'

    Returns:
        category_id string. Falls back to candidates[0] if LLM response is unparsable.
    """
    if not candidates:
        raise ValueError("pick_best_category: no candidates provided")
    if len(candidates) == 1:
        return candidates[0]['category_id']

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

    try:
        text = call_vision(image_paths, prompt, max_tokens=200)
    except Exception:
        return candidates[0]['category_id']

    match = re.search(r'MLM\d+', text)
    if not match:
        return candidates[0]['category_id']

    chosen = match.group(0)
    if any(c.get('category_id') == chosen for c in candidates):
        return chosen
    return candidates[0]['category_id']


def analyze_product(image_paths, category_attributes=None, defaults=None, notes=None):
    """
    Analyze product images and generate all MeLi listing content.

    Args:
        image_paths: list of image file paths
        category_attributes: list of attribute dicts from MeLi API (optional)
        defaults: dict of fixed values like {"BRAND": "DAJIBA"} to enforce
        notes: extra context about the product (e.g. "3-pack", "waterproof")

    Returns:
        dict with product_name, family_name, title_alternatives, description,
        attributes, search_keywords
    """
    defaults = defaults or {}

    # Build the attribute list if we have category data
    attr_instructions = ""
    if category_attributes:
        attr_list = []
        for attr in category_attributes:
            attr_id = attr.get('id', '')
            name = attr.get('name', '')
            values = attr.get('values', [])
            value_type = attr.get('value_type', 'string')
            tags = attr.get('tags', {})

            skip = ['VERTICAL_TAGS', 'DESCRIPTIVE_TAGS', 'PRODUCT_DATA_SOURCE',
                    'SELLER_PACKAGE_DATA_SOURCE', 'PACKAGE_DATA_SOURCE', 'SYI_PYMES_ID',
                    'EXCLUDED_PLATFORMS', 'LIMITED_MARKETPLACE_VISIBILITY_REASONS',
                    'SEARCH_ENHANCEMENT_FIELDS', 'CATALOG_TITLE', 'IS_NEW_OFFER',
                    'ADDITIONAL_INFO_REQUIRED', 'EMPTY_GTIN_REASON']
            if attr_id in skip:
                continue
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

    defaults_text = ""
    if defaults:
        defaults_text = f"""
FIXED VALUES (already set, do not include these in attributes):
{json.dumps(defaults, ensure_ascii=False, indent=2)}
"""

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
- Use \\n for line breaks and \\n\\n for blank lines between bullet points.
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

    text = call_vision(image_paths, prompt, max_tokens=4000, json_output=True)

    # Parse JSON from response (model might wrap it in markdown code blocks)
    try:
        start = text.index('{')
        end = text.rindex('}') + 1
        data = json.loads(text[start:end])
    except (ValueError, json.JSONDecodeError) as e:
        raise Exception(f"Failed to parse LLM response as JSON: {e}\nRaw: {text[:500]}")

    # Merge defaults into attributes
    if defaults:
        for k, v in defaults.items():
            if k not in data.get('attributes', {}):
                data['attributes'][k] = v

    # Append standard footer to description
    warranty = defaults.get('WARRANTY_TIME', '30 días')
    footer = (
        "\n\nENVIO:\n\nEnviamos a toda la Republica Mexicana con Mercado Envios."
        f"\n\nGARANTIA:\n\nProducto nuevo con garantia de {warranty}."
        "\n\nSi tienes alguna duda, no dudes en preguntar."
    )
    if 'description' in data:
        data['description'] = data['description'] + footer

    return data
