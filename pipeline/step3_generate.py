# -*- coding: utf-8 -*-
"""
Step 3: Image generation — sends Step 2's English prompts + reference photo
to the image model (gemini-3-pro-image-preview) and saves PNGs.

Key differences from old generate-all-parallel.py:
  - Input is Step 2's English prompt (not Chinese brief)
  - Default aspect ratio 3:4 (not 1:1)
  - Default resolution 2K (not 1K)
  - Prompt already contains all fidelity constraints from Step 2
"""
import os
import time
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from google.genai import types

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from vertex_client import get_client, GENERATION_MODEL
from pipeline.config import DEFAULTS
from pipeline.retry import with_retry

def _get_client():
    return get_client()


def _detect_mime(path):
    with open(path, 'rb') as f:
        h = f.read(4)
    return 'image/jpeg' if h[:2] == b'\xff\xd8' else 'image/png'


def _aspect_to_config(aspect_ratio):
    """Convert aspect ratio string to Gemini image config value."""
    # Gemini accepts these exact strings
    mapping = {
        '1:1': '1:1', '2:3': '2:3', '3:2': '3:2',
        '3:4': '3:4', '4:3': '4:3', '4:5': '4:5', '5:4': '5:4',
        '9:16': '9:16', '16:9': '16:9',
    }
    return mapping.get(aspect_ratio, '3:4')


def _size_to_config(image_size):
    """Convert image size string to Gemini output size hint."""
    # Gemini uses these: 256, 512, 1024, 2048
    mapping = {'0.5K': '512', '1K': '1024', '2K': '2048', '4K': '2048'}
    return mapping.get(image_size, '2048')


@with_retry(max_retries=2, base_delay=20)
def generate_one(ref_path, english_prompt, output_path,
                 aspect_ratio='3:4', image_size='2K'):
    """
    Generate a single image.

    Args:
        ref_path: path to reference product photo
        english_prompt: Step 2's expanded English prompt (250-350 words)
        output_path: where to save the PNG
        aspect_ratio: e.g. '3:4', '1:1'
        image_size: e.g. '2K', '1K'

    Returns:
        True if successful, False otherwise
    """
    try:
        with open(ref_path, 'rb') as f:
            ref_part = types.Part.from_bytes(
                data=f.read(),
                mime_type=_detect_mime(ref_path),
            )

        client = _get_client()
        resp = client.models.generate_content(
            model=GENERATION_MODEL,
            config=types.GenerateContentConfig(
                response_modalities=['IMAGE'],
                image_config=types.ImageConfig(
                    aspect_ratio=_aspect_to_config(aspect_ratio),
                ),
            ),
            contents=[english_prompt, ref_part],
        )

        # Extract image from response
        for part in resp.candidates[0].content.parts:
            if part.inline_data and part.inline_data.mime_type.startswith('image/'):
                Path(output_path).parent.mkdir(parents=True, exist_ok=True)
                ext = 'png' if 'png' in part.inline_data.mime_type else 'jpg'
                out = str(output_path)
                if not out.endswith(f'.{ext}'):
                    out = out.rsplit('.', 1)[0] + f'.{ext}' if '.' in out else out + f'.{ext}'
                with open(out, 'wb') as f:
                    f.write(part.inline_data.data)
                return True
        return False
    except Exception as e:
        print(f'  [generate] ERR: {type(e).__name__}: {str(e)[:200]}')
        return False


def generate_all(ref_path, expanded_prompts, output_dir,
                 aspect_ratio=None, image_size=None, max_workers=5):
    """
    Generate all images in parallel.

    Args:
        ref_path: path to reference product photo
        expanded_prompts: list of {prompt: "..."} from Step 2
        output_dir: directory to save images
        aspect_ratio: override (default from config)
        image_size: override (default from config)
        max_workers: parallel workers

    Returns:
        list of output paths (None for failed images)
    """
    ar = aspect_ratio or DEFAULTS['aspect_ratio']
    sz = image_size or DEFAULTS['image_size']
    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    results = [None] * len(expanded_prompts)

    def _task(idx, prompt_obj):
        prompt_text = prompt_obj.get('prompt', '') if isinstance(prompt_obj, dict) else str(prompt_obj)
        out_path = out_dir / f'img-{idx+1:02d}.png'
        t0 = time.time()
        ok = generate_one(ref_path, prompt_text, str(out_path), ar, sz)
        elapsed = time.time() - t0
        status = '✓' if ok else '✗'
        print(f'  [{status}] Image {idx+1}/{len(expanded_prompts)} ({elapsed:.1f}s)', flush=True)
        return idx, str(out_path) if ok else None

    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        futures = [pool.submit(_task, i, p) for i, p in enumerate(expanded_prompts)]
        for fut in as_completed(futures):
            idx, path = fut.result()
            results[idx] = path

    return results


if __name__ == '__main__':
    import json
    import sys as _sys
    _sys.stdout.reconfigure(encoding='utf-8')
    if len(_sys.argv) < 3:
        print('Usage: python -m pipeline.step3_generate <ref_image> <expanded_prompts.json> [output_dir]')
        _sys.exit(1)
    ref = _sys.argv[1]
    with open(_sys.argv[2], encoding='utf-8') as f:
        prompts = json.load(f)
    out = _sys.argv[3] if len(_sys.argv) > 3 else 'output'
    paths = generate_all(ref, prompts, out)
    print(f'\nGenerated: {sum(1 for p in paths if p)}/{len(prompts)}')
