# -*- coding: utf-8 -*-
"""
Generate ALL images for comparison-v2: 8 per product × 10 products × 2 sources = 160 images
Uses parallel generation (concurrent.futures) to maximize throughput
"""
import sys, io, json, os, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from concurrent.futures import ThreadPoolExecutor, as_completed
from google import genai
from google.genai import types

GEMINI_KEY = os.environ.get('GEMINI_API_KEY', '')
gemini = genai.Client(api_key=GEMINI_KEY)
BASE_DIR = 'evals/comparison-v2'

def generate_one(args):
    product_idx, source, img_idx, specs, brief, ref_bytes, out_path = args
    if os.path.exists(out_path):
        return (product_idx, source, img_idx, 'CACHED')
    try:
        ref_part = types.Part.from_bytes(data=ref_bytes, mime_type='image/jpeg')
        resp = gemini.models.generate_content(
            model='gemini-3-pro-image-preview',
            config=types.GenerateContentConfig(
                response_modalities=['IMAGE'],
                system_instruction=specs + "\n\n请根据以上参考照片中的真实产品，生成一张1:1正方形的电商产品场景图。必须严格还原产品的真实外观、结构和细节，不得添加或省略任何部件。",
                image_config=types.ImageConfig(image_size='2K', aspect_ratio='1:1'),
            ),
            contents=[ref_part, brief],
        )
        for part in resp.candidates[0].content.parts:
            if part.inline_data:
                with open(out_path, 'wb') as f:
                    f.write(part.inline_data.data)
                return (product_idx, source, img_idx, 'OK')
        return (product_idx, source, img_idx, 'NO_IMG')
    except Exception as e:
        return (product_idx, source, img_idx, f'ERR:{str(e)[:80]}')

# Build all tasks
tasks = []
for idx in range(1, 11):
    pname = f'product-{idx:02d}'
    d = f'{BASE_DIR}/{pname}'
    ref_path = f'test-products/stationery/{pname}.jpg'
    
    if not os.path.exists(ref_path):
        continue
    
    with open(ref_path, 'rb') as f:
        ref_bytes = f.read()
    
    for source in ['picset', 'ours']:
        plan_file = f'{d}/{source}-plan.json'
        if not os.path.exists(plan_file):
            plan_file = f'{d}/our-plan.json' if source == 'ours' else plan_file
        if not os.path.exists(plan_file):
            print(f'SKIP {pname}/{source}: no plan')
            continue
        
        with open(plan_file, encoding='utf-8') as f:
            plan = json.load(f)
        
        specs = plan.get('design_specs', '')
        images = plan.get('images', [])
        
        for i, img in enumerate(images[:8], 1):
            out_path = f'{d}/{source}-img-{i}.png'
            tasks.append((idx, source, i, specs, img['design_content'], ref_bytes, out_path))

print(f'Total tasks: {len(tasks)}')
cached = sum(1 for t in tasks if os.path.exists(t[6]))
print(f'Cached: {cached}, To generate: {len(tasks) - cached}', flush=True)

# Run parallel - 5 concurrent to stay well under 150 RPM
t0 = time.time()
completed = 0
errors = 0

with ThreadPoolExecutor(max_workers=5) as executor:
    futures = {executor.submit(generate_one, task): task for task in tasks}
    for future in as_completed(futures):
        result = future.result()
        completed += 1
        status = result[3]
        if status.startswith('ERR'):
            errors += 1
        elapsed = time.time() - t0
        rate = completed / elapsed * 60 if elapsed > 0 else 0
        print(f'[{completed}/{len(tasks)}] P{result[0]:02d}/{result[1]}/img-{result[2]}: {status} ({elapsed:.0f}s, {rate:.0f}/min)', flush=True)

total_time = time.time() - t0
print(f'\nDONE: {completed} tasks in {total_time:.0f}s ({completed/total_time*60:.0f}/min), {errors} errors')
