# -*- coding: utf-8 -*-
"""
MercaFlow Pipeline Orchestrator — runs all 4 steps end-to-end.

Usage:
    python -m pipeline.run <image_path> [options]

Options:
    --type detail|main       Image type (default: detail)
    --count N                Number of images (default: 8 for detail, 4 for main)
    --lang CODE              Target language (default: none)
    --requirements TEXT      Requirements text (or path to .txt file)
    --ratio RATIO            Aspect ratio (default: 3:4)
    --size SIZE              Image size (default: 2K)
    --output DIR             Output directory (default: output/<timestamp>)
    --skip-generate          Only run analysis + expansion, skip image generation
    --workers N              Parallel workers for generation (default: 5)
"""
import argparse
import json
import time
import os
import sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent))
sys.stdout.reconfigure(encoding='utf-8')

from pipeline.config import DEFAULTS
from pipeline.step0_ai_write import ai_write, auto_select
from pipeline.step1_analyze import analyze
from pipeline.step2_expand import expand
from pipeline.step3_generate import generate_all


def run_pipeline(image_paths, image_type='detail', image_count=None,
                 target_language='none', requirements='',
                 aspect_ratio=None, image_size=None,
                 output_dir=None, skip_generate=False, max_workers=5):
    """
    Run the full 4-step pipeline.

    Returns dict with all intermediate results + output paths.
    """
    if image_count is None:
        image_count = 8 if image_type == 'detail' else 4

    ar = aspect_ratio or DEFAULTS['aspect_ratio']
    sz = image_size or DEFAULTS['image_size']
    ts = datetime.now().strftime('%Y%m%d_%H%M%S')
    out_dir = Path(output_dir or f'output/{ts}_{image_type}_{image_count}img')
    out_dir.mkdir(parents=True, exist_ok=True)

    result = {
        'params': {
            'image_type': image_type,
            'image_count': image_count,
            'target_language': target_language,
            'aspect_ratio': ar,
            'image_size': sz,
            'requirements': requirements[:200] + '...' if len(requirements) > 200 else requirements,
        },
        'output_dir': str(out_dir),
    }

    # ── Step 0: AI帮写 (auto-generate requirements if not provided) ──
    t0 = time.time()
    if not requirements:
        print(f'═══ Step 0: AI帮写 ({image_type}) ═══', flush=True)
        t_s0 = time.time()
        options = ai_write(image_paths, image_type=image_type)
        print(f'  Generated {len(options)} style options:', flush=True)
        for i, opt in enumerate(options):
            name = ''
            text = opt.get('prompt_text', str(opt))
            for line in text.split('\n'):
                if '风格名称' in line:
                    name = line.split('：')[-1].split(':')[-1].strip()
                    break
            print(f'  {chr(65+i)}. {name or f"Option {i}"}', flush=True)

        requirements, selected_idx, reason = auto_select(options, image_paths, image_type)
        t_e0 = time.time()
        print(f'  Auto-selected: Option {chr(65+selected_idx)} — {reason}', flush=True)
        print(f'  Done in {t_e0-t_s0:.1f}s', flush=True)

        # Save all options + selection
        with open(out_dir / 'step0_options.json', 'w', encoding='utf-8') as f:
            json.dump({
                'options': [o.get('prompt_text', str(o)) for o in options],
                'selected': selected_idx,
                'reason': reason,
            }, f, ensure_ascii=False, indent=2)

        result['ai_write'] = {
            'n_options': len(options),
            'selected': selected_idx,
            'reason': reason,
            'elapsed_s': round(t_e0-t_s0, 1),
        }
    else:
        print(f'═══ Step 0: Skipped (requirements provided) ═══', flush=True)

    # ── Step 1: Analyze ──
    print(f'\n═══ Step 1: Analyze ({image_type}, {image_count} images, lang={target_language}) ═══', flush=True)
    t1_start = time.time()
    analysis = analyze(
        image_paths=image_paths,
        image_type=image_type,
        image_count=image_count,
        target_language=target_language,
        requirements=requirements,
    )
    t1 = time.time()

    # Save analysis result
    with open(out_dir / 'step1_analysis.json', 'w', encoding='utf-8') as f:
        json.dump(analysis, f, ensure_ascii=False, indent=2)

    n_images = len(analysis.get('images', []))
    is_complex = analysis.get('is_complex_product', False)
    print(f'  Done in {t1-t1_start:.1f}s — {n_images} images planned, complex={is_complex}', flush=True)
    for i, img in enumerate(analysis.get('images', []), 1):
        print(f'  {i}. {img.get("title", "?")}', flush=True)

    result['analysis'] = {
        'is_complex_product': is_complex,
        'n_images': n_images,
        'elapsed_s': round(t1-t1_start, 1),
    }

    # ── Step 2: Expand ──
    print(f'\n═══ Step 2: Expand (Chinese → English structured prompts) ═══', flush=True)
    t2 = time.time()
    expanded = expand(
        analysis_result=analysis,
        target_language=target_language,
        image_type=image_type,
    )
    t3 = time.time()

    # Save expanded prompts
    with open(out_dir / 'step2_expanded.json', 'w', encoding='utf-8') as f:
        json.dump(expanded, f, ensure_ascii=False, indent=2)

    print(f'  Done in {t3-t2:.1f}s — {len(expanded)} prompts generated', flush=True)
    for i, p in enumerate(expanded, 1):
        text = p.get('prompt', str(p))[:80] if isinstance(p, dict) else str(p)[:80]
        print(f'  {i}. {text}...', flush=True)

    result['expansion'] = {
        'n_prompts': len(expanded),
        'elapsed_s': round(t3-t2, 1),
    }

    if skip_generate:
        print(f'\n═══ Skipping Step 3 (--skip-generate) ═══', flush=True)
        result['images'] = None
        _save_summary(result, out_dir)
        return result

    # ── Step 3: Generate ──
    print(f'\n═══ Step 3: Generate ({len(expanded)} images, {ar}, {sz}, {max_workers} workers) ═══', flush=True)
    t4 = time.time()
    paths = generate_all(
        ref_path=image_paths[0],
        expanded_prompts=expanded,
        output_dir=str(out_dir / 'images'),
        aspect_ratio=ar,
        image_size=sz,
        max_workers=max_workers,
    )
    t5 = time.time()

    n_ok = sum(1 for p in paths if p)
    print(f'  Done in {t5-t4:.1f}s — {n_ok}/{len(paths)} images generated', flush=True)

    result['generation'] = {
        'n_success': n_ok,
        'n_total': len(paths),
        'elapsed_s': round(t5-t4, 1),
        'paths': paths,
    }

    _save_summary(result, out_dir)
    total = time.time() - t0
    print(f'\n═══ Pipeline complete ({total:.1f}s total) ═══', flush=True)
    print(f'  Output: {out_dir}', flush=True)
    return result


def _save_summary(result, out_dir):
    with open(Path(out_dir) / 'pipeline_summary.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)


def main():
    parser = argparse.ArgumentParser(description='MercaFlow Pipeline')
    parser.add_argument('image', help='Product image path')
    parser.add_argument('--type', default='detail', choices=['detail', 'main'])
    parser.add_argument('--count', type=int, default=None)
    parser.add_argument('--lang', default='none')
    parser.add_argument('--requirements', default='')
    parser.add_argument('--ratio', default='3:4')
    parser.add_argument('--size', default='2K')
    parser.add_argument('--output', default=None)
    parser.add_argument('--skip-generate', action='store_true')
    parser.add_argument('--workers', type=int, default=5)
    args = parser.parse_args()

    # If requirements points to a file, read it
    reqs = args.requirements
    if reqs and os.path.isfile(reqs):
        with open(reqs, encoding='utf-8') as f:
            reqs = f.read().strip()

    run_pipeline(
        image_paths=[args.image],
        image_type=args.type,
        image_count=args.count,
        target_language=args.lang,
        requirements=reqs,
        aspect_ratio=args.ratio,
        image_size=args.size,
        output_dir=args.output,
        skip_generate=args.skip_generate,
        max_workers=args.workers,
    )


if __name__ == '__main__':
    main()
