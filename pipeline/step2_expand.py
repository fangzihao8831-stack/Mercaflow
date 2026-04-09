# -*- coding: utf-8 -*-
"""
Step 2: Prompt expansion — Chinese briefs → structured English prompts.

Takes Step 1's output (design_specs + images[]) and produces one
250-350 word English prompt per image, following the 11-element structure.

Uses PicSet's exact generator template from prompts/picset-generator-template.txt
with dynamic [Design Specifications] + [Image Plans] sections appended.
"""
import json
from pathlib import Path
from google.genai import types

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from vertex_client import get_client, PLANNING_MODEL
from pipeline.retry import with_retry

PROMPTS_DIR = Path(__file__).parent.parent / 'prompts'

# Load the static generator template once
_GENERATOR_TEMPLATE = (PROMPTS_DIR / 'picset-generator-template.txt').read_text(encoding='utf-8')

_client = None
def _get_client():
    global _client
    if _client is None:
        _client = get_client()
    return _client


def _build_dynamic_input(analysis_result):
    """
    Build the [Design Specifications] + [Image Plans] sections
    from Step 1's output, to be appended after the static template.
    """
    lines = []

    # Section 1: Design Specifications
    lines.append('[Design Specifications]')
    lines.append(analysis_result.get('design_specs', ''))
    lines.append('')

    # Section 2: Image Plans
    lines.append('[Image Plans]')
    for i, img in enumerate(analysis_result.get('images', []), 1):
        title = img.get('title', f'Image {i}')
        design_content = img.get('design_content', '')
        lines.append(f'### Image {i}: {title}')
        lines.append(design_content)
        lines.append('')

    return '\n'.join(lines)


@with_retry(max_retries=3, base_delay=15)
def expand(analysis_result, target_language='none', image_type='detail'):
    """
    Run Step 2 prompt expansion.

    Args:
        analysis_result: dict from Step 1 (must have design_specs + images[])
        target_language: passed through for context
        image_type: 'detail' or 'main'

    Returns:
        list of dicts [{prompt: "250-350 word English prompt"}, ...]
    """
    # Build the full prompt: static template + dynamic input
    dynamic_input = _build_dynamic_input(analysis_result)
    full_prompt = _GENERATOR_TEMPLATE + '\n\n' + dynamic_input

    client = _get_client()
    resp = client.models.generate_content(
        model=PLANNING_MODEL,
        config=types.GenerateContentConfig(
            temperature=0.4,
            max_output_tokens=8192,
            response_mime_type='application/json',
        ),
        contents=[full_prompt],
    )

    prompts = json.loads(resp.text)

    # Validate: should be a list of {prompt: "..."} dicts
    if isinstance(prompts, list):
        return prompts
    # Some models return {prompts: [...]} or {generated_prompts: [...]}
    if isinstance(prompts, dict):
        for key in ('prompts', 'generated_prompts'):
            if key in prompts and isinstance(prompts[key], list):
                return prompts[key]
        # Maybe it's a single prompt wrapped in dict
        if 'prompt' in prompts:
            return [prompts]
    return prompts


if __name__ == '__main__':
    import sys as _sys
    _sys.stdout.reconfigure(encoding='utf-8')
    if len(_sys.argv) < 2:
        print('Usage: python -m pipeline.step2_expand <analysis_result.json>')
        _sys.exit(1)
    with open(_sys.argv[1], encoding='utf-8') as f:
        analysis = json.load(f)
    prompts = expand(analysis)
    print(json.dumps(prompts, ensure_ascii=False, indent=2))
