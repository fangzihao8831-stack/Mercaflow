# -*- coding: utf-8 -*-
"""
MercaFlow Step 0: Product analyzer.
Looks at a product photo and produces a 详情图要求 text that gets injected
into the planning prompt's {REQUIREMENTS} placeholder.

Replaces the old hardcoded one-liner. Adds product-specific physical
constraints (thickness, binding, material) that the planner cannot infer
from a flat 2D catalog photo alone — this is what prevents the
thin-booklet → thick-book hallucination.

Usage:
    from product_analyzer import analyze_product
    requirements_text = analyze_product('path/to/product.jpg')
    # → 'Product type: ...\\nPhysical features: ...\\n...'
"""
import os
from pathlib import Path
from google.genai import types
from vertex_client import get_client

ANALYZER_MODEL = os.environ.get('ANALYZER_MODEL', 'gemini-3-flash-preview')
ANALYZER_PROMPT_PATH = Path(__file__).parent / 'prompts' / 'product-analysis-prompt.txt'

# Load once at import — single source of truth
with open(ANALYZER_PROMPT_PATH, encoding='utf-8') as f:
    ANALYZER_PROMPT = f.read()

# Lazy client
_client = None
def _get_client():
    global _client
    if _client is None:
        _client = get_client()
    return _client


def _detect_mime(path):
    with open(path, 'rb') as f:
        h = f.read(4)
    return 'image/jpeg' if h[:2] == b'\xff\xd8' else 'image/png'


# Fallback used when Step 0 fails — same as the old hardcoded string
FALLBACK_REQUIREMENTS = '无文案纯视觉设计，目标平台MercadoLibre拉丁美洲市场'


def analyze_product(image_path):
    """
    Analyze a product photo and return a 详情图要求 text suitable for
    injection into the planning prompt's {REQUIREMENTS} placeholder.
    
    Returns a plain string. On failure, returns FALLBACK_REQUIREMENTS so
    the pipeline never breaks.
    """
    try:
        with open(image_path, 'rb') as f:
            ref_part = types.Part.from_bytes(
                data=f.read(),
                mime_type=_detect_mime(image_path),
            )

        client = _get_client()
        resp = client.models.generate_content(
            model=ANALYZER_MODEL,
            config=types.GenerateContentConfig(
                temperature=0.2,            # mostly deterministic, slight room for product judgment
                max_output_tokens=1024,
                system_instruction=ANALYZER_PROMPT,
            ),
            contents=[
                '【产品参考照片】：',
                ref_part,
                '请按 6 步流程分析产品，输出符合要求的纯文本详情图要求。',
            ],
        )

        text = resp.text.strip()
        # Strip code fences if the model accidentally wrapped output
        if text.startswith('```'):
            lines = text.split('\n')
            text = '\n'.join(lines[1:-1] if lines[-1].startswith('```') else lines[1:])
        return text or FALLBACK_REQUIREMENTS

    except Exception as e:
        print(f'  [analyzer] ERR: {type(e).__name__}: {str(e)[:100]} — using fallback')
        return FALLBACK_REQUIREMENTS


if __name__ == '__main__':
    # CLI smoke test: python product_analyzer.py <image>
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    if len(sys.argv) != 2:
        print('Usage: python product_analyzer.py <image_path>')
        sys.exit(1)
    print(analyze_product(sys.argv[1]))
