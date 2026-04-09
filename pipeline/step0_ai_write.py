# -*- coding: utf-8 -*-
"""
Step 0: AI帮写 — generates 3 style options from product photo only.
In automation mode, LLM auto-selects the best option.
In UI mode (future), user picks manually.
"""
import json
from pathlib import Path
from google.genai import types

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from vertex_client import get_client, PLANNING_MODEL
from pipeline.retry import with_retry

PROMPTS_DIR = Path(__file__).parent.parent / 'prompts'

_DETAIL_TEMPLATE = (PROMPTS_DIR / 'picset-ai-write-detail-prompt.txt').read_text(encoding='utf-8')
_MAIN_TEMPLATE = (PROMPTS_DIR / 'picset-ai-write-main-prompt.txt').read_text(encoding='utf-8')

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


@with_retry(max_retries=3, base_delay=15)
def ai_write(image_paths, image_type='detail'):
    """
    Generate 3 style options from product photos.

    Args:
        image_paths: list of product image paths (1-6)
        image_type: 'detail' or 'main'

    Returns:
        list of 3 dicts, each with 'prompt_text' field (markdown string)
    """
    template = _MAIN_TEMPLATE if image_type == 'main' else _DETAIL_TEMPLATE

    contents = [template]
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
            max_output_tokens=8192,
            response_mime_type='application/json',
        ),
        contents=contents,
    )

    result = json.loads(resp.text)
    # Result should be {"options": [{prompt_text: "..."}, ...]}
    if isinstance(result, dict) and 'options' in result:
        return result['options']
    if isinstance(result, list):
        return result
    return [result]


def auto_select(options, image_paths, image_type='detail'):
    """
    Let LLM pick the best option from 3 alternatives.
    Always returns tuple: (prompt_text, selected_idx, reason)
    """
    if not options:
        return '', 0, 'no options generated'
    if len(options) == 1:
        return options[0].get('prompt_text', str(options[0])), 0, 'only one option'

    # Build a selection prompt
    selection_prompt = f"""你是电商视觉策划总监。以下是 AI 为一款产品生成的 {len(options)} 套{"主图" if image_type == "main" else "详情图"}设计方案。

请选出最适合电商平台销售的方案（考虑：视觉吸引力、卖点清晰度、配色商业感、目标人群精准度）。

只返回 JSON：{{"selected": 0-{len(options)-1}的数字, "reason": "一句话理由"}}

"""
    for i, opt in enumerate(options):
        text = opt.get('prompt_text', str(opt))
        selection_prompt += f'\n--- 方案 {i} ---\n{text}\n'

    import time
    client = _get_client()
    try:
        time.sleep(2)  # small delay to avoid rate limiting after ai_write call
        resp = client.models.generate_content(
            model=PLANNING_MODEL,
            config=types.GenerateContentConfig(
                temperature=0.0,
                max_output_tokens=256,
                response_mime_type='application/json',
            ),
            contents=[selection_prompt],
        )
        choice = json.loads(resp.text)
        idx = int(choice.get('selected', 0))
        reason = choice.get('reason', '')
        idx = max(0, min(idx, len(options) - 1))
    except Exception as e:
        idx = 0
        reason = f'auto-select failed ({type(e).__name__}), defaulting to option A'

    selected = options[idx]
    return selected.get('prompt_text', str(selected)), idx, reason


if __name__ == '__main__':
    import sys as _sys
    _sys.stdout.reconfigure(encoding='utf-8')
    if len(_sys.argv) < 2:
        print('Usage: python -m pipeline.step0_ai_write <image> [detail|main]')
        _sys.exit(1)
    img = _sys.argv[1]
    it = _sys.argv[2] if len(_sys.argv) > 2 else 'detail'
    options = ai_write([img], image_type=it)
    print(f'Generated {len(options)} options:\n')
    for i, opt in enumerate(options):
        print(f'=== Option {i} ===')
        print(opt.get('prompt_text', str(opt))[:500])
        print()
    text, idx, reason = auto_select(options, [img], image_type=it)
    print(f'Auto-selected: Option {idx} — {reason}')
