# -*- coding: utf-8 -*-
"""
MercaFlow image evaluator — Vertex AI / Gemini Flash version.
Replaces the old Claude OAuth evaluator. Uses prompts/evaluator-prompt.txt
as the single source of truth for the evaluation logic.

Usage:
    from evaluator import score_image
    result = score_image('path/to/ref.jpg', 'path/to/generated.png')
    # result is a dict matching the JSON schema in evaluator-prompt.txt
"""
import os
import json
from pathlib import Path
from google.genai import types
from vertex_client import get_client

EVALUATOR_MODEL = os.environ.get('EVALUATOR_MODEL', 'gemini-3-flash-preview')
EVALUATOR_PROMPT_PATH = Path(__file__).parent / 'prompts' / 'evaluator-prompt.txt'

# Load the prompt once at import time — single source of truth
with open(EVALUATOR_PROMPT_PATH, encoding='utf-8') as f:
    EVALUATOR_PROMPT = f.read()

# Lazy client (one per process)
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


def score_image(ref_path, gen_path):
    """
    Compare a reference photo to an AI-generated image and return a strict eval.
    
    Returns a dict with the schema defined in prompts/evaluator-prompt.txt:
        {
          product_identification, reference_properties, generated_properties,
          differences[], physical_match, structure_match, identity_match,
          self_check, final_score, critical_issue, verdict
        }
    
    On API/parse error, returns:
        {final_score: -1, error: "...", verdict: "reject"}
    """
    try:
        with open(ref_path, 'rb') as f:
            ref_part = types.Part.from_bytes(
                data=f.read(),
                mime_type=_detect_mime(ref_path),
            )
        with open(gen_path, 'rb') as f:
            gen_part = types.Part.from_bytes(
                data=f.read(),
                mime_type=_detect_mime(gen_path),
            )

        client = _get_client()
        resp = client.models.generate_content(
            model=EVALUATOR_MODEL,
            config=types.GenerateContentConfig(
                temperature=0.0,             # deterministic, no creativity
                max_output_tokens=4096,      # roomy enough for the full schema
                response_mime_type='application/json',
                system_instruction=EVALUATOR_PROMPT,
            ),
            contents=[
                '【参考照片】（顾客实际收到的产品应该长这样）：',
                ref_part,
                '【AI 生成图片】（需要质检的图片）：',
                gen_part,
                '请按 8 步流程严格评估，输出符合要求的 JSON。',
            ],
        )

        return json.loads(resp.text)

    except json.JSONDecodeError as e:
        return {
            'final_score': -1,
            'verdict': 'reject',
            'error': f'JSON parse failed: {e}',
            'raw_text': resp.text[:500] if 'resp' in locals() else None,
        }
    except Exception as e:
        return {
            'final_score': -1,
            'verdict': 'reject',
            'error': f'{type(e).__name__}: {str(e)[:200]}',
        }


if __name__ == '__main__':
    # CLI smoke test: python evaluator.py <ref.jpg> <generated.png>
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    if len(sys.argv) != 3:
        print('Usage: python evaluator.py <ref_image> <generated_image>')
        sys.exit(1)
    result = score_image(sys.argv[1], sys.argv[2])
    print(json.dumps(result, ensure_ascii=False, indent=2))
