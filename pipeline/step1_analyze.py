# -*- coding: utf-8 -*-
"""
Step 1: Product analysis — generates design_specs + per-image briefs.

Uses PicSet's exact analysis prompts with dynamic templating:
  - {IMAGE_COUNT} → "正好 N 张"
  - {TARGET_LANG} → language display name in the design_content template
  - requirements prefix → "注意所有图片不要有设计文案" when target_language=none
"""
import json
from pathlib import Path
from google.genai import types

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from vertex_client import get_client, PLANNING_MODEL
from pipeline.config import LANG_MAP, NO_TEXT_PREFIX
from pipeline.retry import with_retry

PROMPTS_DIR = Path(__file__).parent.parent / 'prompts'

# Load both analysis prompt templates once
_DETAIL_TEMPLATE = (PROMPTS_DIR / 'picset-detail-analysis-prompt.txt').read_text(encoding='utf-8')
_MAIN_TEMPLATE = (PROMPTS_DIR / 'picset-main-analysis-prompt.txt').read_text(encoding='utf-8')

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


def _render_prompt(image_type, image_count, target_language, requirements):
    """Render the analysis prompt with dynamic substitutions."""
    template = _MAIN_TEMPLATE if image_type == 'main' else _DETAIL_TEMPLATE
    lang_display = LANG_MAP.get(target_language, target_language)

    # 1. Replace image count: "正好 8 张" → "正好 N 张"
    import re
    original = template
    template = re.sub(r'\*\*正好\s*\d+\s*张\*\*', f'**正好 {image_count} 张**', template)
    template = re.sub(r'\*\*正好\s*\d+\s*个\*\*', f'**正好 {image_count} 个**', template)
    if template == original:
        print(f'  [WARN] image count regex did not match — template may have unexpected format', flush=True)

    # 2. Replace target language in design_content template
    #    Pattern: "（使用 无文字(纯视觉)）" or "（使用 英语）"
    template = re.sub(r'（使用 [^）]+）', f'（使用 {lang_display}）', template)

    # 3. Replace in the rules section: "目标输出语言：无文字(纯视觉)" etc.
    template = re.sub(r'目标输出语言[：:]\s*[^\n。]+', f'目标输出语言：{lang_display}', template)

    # 4. Prepare requirements with prefix
    if target_language == 'none':
        full_req = NO_TEXT_PREFIX + requirements
    else:
        full_req = requirements

    # 5. Replace the trailing "用户需求描述：..." line
    template = re.sub(r'用户需求描述：.*$', f'用户需求描述：{full_req}', template, flags=re.DOTALL)

    return template


@with_retry(max_retries=3, base_delay=15)
def analyze(image_paths, image_type='detail', image_count=8,
            target_language='none', requirements=''):
    """
    Run Step 1 analysis on product image(s).

    Args:
        image_paths: list of image file paths (1-6)
        image_type: 'detail' or 'main'
        image_count: how many images to plan (1-15)
        target_language: language code ('none', 'en', 'es', etc.)
        requirements: user requirements text or AI帮写 prompt_text

    Returns:
        dict with {is_complex_product, design_specs, images[]}
    """
    prompt = _render_prompt(image_type, image_count, target_language, requirements)

    # Build contents: prompt text + product images
    contents = [prompt]
    for i, img_path in enumerate(image_paths, 1):
        contents.append(f'This is product image {i} of {len(image_paths)}:')
        with open(img_path, 'rb') as f:
            contents.append(types.Part.from_bytes(
                data=f.read(),
                mime_type=_detect_mime(img_path),
            ))

    client = _get_client()
    resp = client.models.generate_content(
        model=PLANNING_MODEL,
        config=types.GenerateContentConfig(
            temperature=0.4,
            max_output_tokens=8192 if image_count <= 5 else 16384,
            response_mime_type='application/json',
        ),
        contents=contents,
    )

    result = json.loads(resp.text)
    result['_meta'] = {
        'image_type': image_type,
        'image_count': image_count,
        'target_language': target_language,
        'model': PLANNING_MODEL,
    }
    return result


if __name__ == '__main__':
    import sys as _sys
    _sys.stdout.reconfigure(encoding='utf-8')
    if len(_sys.argv) < 2:
        print('Usage: python -m pipeline.step1_analyze <image> [image_type] [count] [lang] [requirements]')
        _sys.exit(1)
    img = _sys.argv[1]
    it = _sys.argv[2] if len(_sys.argv) > 2 else 'detail'
    ic = int(_sys.argv[3]) if len(_sys.argv) > 3 else 3
    lang = _sys.argv[4] if len(_sys.argv) > 4 else 'none'
    reqs = _sys.argv[5] if len(_sys.argv) > 5 else ''
    result = analyze([img], image_type=it, image_count=ic, target_language=lang, requirements=reqs)
    print(json.dumps(result, ensure_ascii=False, indent=2))
