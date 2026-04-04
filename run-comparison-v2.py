# -*- coding: utf-8 -*-
"""
MercaFlow Comparison v2 — PicSet's exact prompt, 8 images, all 10 products
PicSet analysis (free) vs Our Gemini Flash (same prompt) → both generate with Gemini Pro
"""
import sys, io, json, requests, time, os, base64
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import oss2
from google import genai
from google.genai import types

# === KEYS ===
ANON_KEY = os.environ.get('PICSET_ANON_KEY', '')
GEMINI_KEY = os.environ.get('GEMINI_API_KEY', '')
CLAUDE_KEY = os.environ.get('ANTHROPIC_OAUTH_KEY', '')

with open('evals/picset-token.json', encoding='utf-8') as f:
    ACCESS_TOKEN = json.loads(f.read())['access_token']

BASE = 'https://picsetai.cn/supabase'
USER_ID = 'bd1ec1fc-56b6-4656-b70d-a7c163fa2895'
gemini = genai.Client(api_key=GEMINI_KEY)
NUM_IMAGES = 8
REQUIREMENTS = '无文案纯视觉设计，目标平台MercadoLibre拉丁美洲市场'

# Load PicSet's exact prompt template
with open('prompts/analysis-prompt.txt', encoding='utf-8') as f:
    PROMPT_TEMPLATE = f.read()

def get_prompt(image_count=NUM_IMAGES, target_lang='无文字(纯视觉)', reqs=REQUIREMENTS):
    return PROMPT_TEMPLATE.replace('{IMAGE_COUNT}', str(image_count)).replace('{TARGET_LANGUAGE}', target_lang).replace('{REQUIREMENTS}', reqs)

def picset_headers():
    return {'Authorization': f'Bearer {ACCESS_TOKEN}', 'apikey': ANON_KEY, 'Content-Type': 'application/json'}

def upload_to_picset(img_path):
    creds = requests.post(f'{BASE}/functions/v1/get-oss-sts', headers=picset_headers(), json={}).json()
    if 'accessKeyId' not in creds:
        raise Exception(f'OSS STS failed: {creds}')
    auth = oss2.StsAuth(creds['accessKeyId'], creds['accessKeySecret'], creds['securityToken'])
    bucket = oss2.Bucket(auth, f'https://{creds["region"]}.aliyuncs.com', creds['bucket'])
    key = f'temp/{USER_ID}/{int(time.time()*1000)}_product_0.png'
    with open(img_path, 'rb') as f:
        bucket.put_object(key, f)
    return key

def picset_analyze(object_key, num_images=NUM_IMAGES):
    resp = requests.post(f'{BASE}/functions/v1/analyze-product-v2', headers=picset_headers(), json={
        'imageType': 'detail', 'imageCount': num_images, 'targetLanguage': 'none',
        'uiLanguage': 'zh-CN', 'productImage': object_key, 'productImages': [object_key],
        'requirements': REQUIREMENTS, 'themeColors': None
    }, timeout=60)
    data = resp.json()
    job_id = data.get('job_id')
    if not job_id:
        return None
    for i in range(60):
        time.sleep(2)
        r = requests.get(f'{BASE}/rest/v1/generation_jobs?select=*&id=eq.{job_id}', headers=picset_headers())
        if r.status_code == 200 and r.json():
            job = r.json()[0]
            if job['status'] == 'success':
                return job['result_data']
            elif job['status'] == 'failed':
                return None
    return None

def our_analyze(img_path, num_images=NUM_IMAGES):
    with open(img_path, 'rb') as f:
        ref = types.Part.from_bytes(data=f.read(), mime_type='image/jpeg')
    prompt = get_prompt(num_images)
    resp = gemini.models.generate_content(
        model='gemini-3-flash-preview',
        config=types.GenerateContentConfig(
            temperature=0.4, max_output_tokens=8192 if num_images <= 5 else 16384,
            response_mime_type='application/json',
        ),
        contents=[prompt, 'This is the product image:', ref],
    )
    return json.loads(resp.text)

def generate_image(system_ctx, brief, ref_part, output_path):
    try:
        resp = gemini.models.generate_content(
            model='gemini-3-pro-image-preview',
            config=types.GenerateContentConfig(
                response_modalities=['IMAGE'],
                system_instruction=system_ctx + "\n\n请根据以上参考照片中的真实产品，生成一张1:1正方形的电商产品场景图。必须严格还原产品的真实外观、结构和细节，不得添加或省略任何部件。",
                image_config=types.ImageConfig(image_size='2K', aspect_ratio='1:1'),
            ),
            contents=[ref_part, brief],
        )
        for part in resp.candidates[0].content.parts:
            if part.inline_data:
                with open(output_path, 'wb') as f:
                    f.write(part.inline_data.data)
                return True
    except Exception as e:
        print(f'    GEN ERR: {e}')
    return False

def detect_mime(path):
    with open(path, 'rb') as f:
        h = f.read(4)
    return 'image/jpeg' if h[:2] == b'\xff\xd8' else 'image/png'

def score_image(ref_path, gen_path):
    with open(ref_path, 'rb') as f: ref_b64 = base64.standard_b64encode(f.read()).decode()
    with open(gen_path, 'rb') as f: gen_b64 = base64.standard_b64encode(f.read()).decode()
    resp = requests.post('https://api.anthropic.com/v1/messages', headers={
        'anthropic-version': '2023-06-01', 'anthropic-beta': 'claude-code-20250219,oauth-2025-04-20',
        'Authorization': f'Bearer {CLAUDE_KEY}', 'Content-Type': 'application/json',
    }, json={
        'model': 'claude-sonnet-4-20250514', 'max_tokens': 300,
        'system': [{'type': 'text', 'text': "You are Claude Code, Anthropic's official CLI for Claude."},
                   {'type': 'text', 'text': '只返回JSON'}],
        'messages': [{'role': 'user', 'content': [
            {'type': 'text', 'text': '参考照片：'},
            {'type': 'image', 'source': {'type': 'base64', 'media_type': detect_mime(ref_path), 'data': ref_b64}},
            {'type': 'text', 'text': 'AI生成图片：'},
            {'type': 'image', 'source': {'type': 'base64', 'media_type': detect_mime(gen_path), 'data': gen_b64}},
            {'type': 'text', 'text': '从顾客角度评分0-100。90+=满意 80-89=微差 70-79=略不同 50-69=投诉 <50=退货。严格评分。返回{"score":N,"issues":["问题"]}'}
        ]}]
    }, timeout=120)
    text = ''.join(b['text'] for b in resp.json().get('content', []) if b.get('type') == 'text')
    try:
        return json.loads(text[text.index('{'):text.rindex('}')+1])
    except:
        return {'score': -1, 'issues': [text[:100]]}

# === MAIN ===
OUT_DIR = 'evals/comparison-v2'
os.makedirs(OUT_DIR, exist_ok=True)
PRODUCTS = [f'test-products/stationery/product-{i:02d}.jpg' for i in range(1, 11)]

all_scores = []

for idx, img_path in enumerate(PRODUCTS, 1):
    if not os.path.exists(img_path):
        print(f'[{idx}/10] SKIP')
        continue

    pname = f'product-{idx:02d}'
    d = f'{OUT_DIR}/{pname}'
    os.makedirs(d, exist_ok=True)

    print(f'\n[{idx}/10] {pname}', flush=True)

    with open(img_path, 'rb') as f:
        ref_part = types.Part.from_bytes(data=f.read(), mime_type='image/jpeg')

    # --- PicSet Analysis (8 images) ---
    picset_plan_path = f'{d}/picset-plan.json'
    if os.path.exists(picset_plan_path):
        with open(picset_plan_path, encoding='utf-8') as f:
            picset_rd = json.load(f)
        print(f'  PicSet: cached ({len(picset_rd["images"])} imgs)', flush=True)
    else:
        print(f'  PicSet: uploading+analyzing...', end=' ', flush=True)
        try:
            obj_key = upload_to_picset(img_path)
            picset_rd = picset_analyze(obj_key, NUM_IMAGES)
            if picset_rd:
                with open(picset_plan_path, 'w', encoding='utf-8') as f:
                    json.dump(picset_rd, f, ensure_ascii=False, indent=2)
                print(f'OK ({len(picset_rd["images"])} imgs)', flush=True)
            else:
                print('FAILED', flush=True)
                picset_rd = None
        except Exception as e:
            print(f'ERR: {e}', flush=True)
            picset_rd = None

    # --- Our Analysis (8 images, same prompt) ---
    our_plan_path = f'{d}/our-plan.json'
    if os.path.exists(our_plan_path):
        with open(our_plan_path, encoding='utf-8') as f:
            our_rd = json.load(f)
        print(f'  Ours: cached ({len(our_rd["images"])} imgs)', flush=True)
    else:
        print(f'  Ours: analyzing...', end=' ', flush=True)
        try:
            our_rd = our_analyze(img_path, NUM_IMAGES)
            with open(our_plan_path, 'w', encoding='utf-8') as f:
                json.dump(our_rd, f, ensure_ascii=False, indent=2)
            print(f'OK ({len(our_rd["images"])} imgs)', flush=True)
        except Exception as e:
            print(f'ERR: {e}', flush=True)
            our_rd = None

    # --- Generate 1st image from each (for scoring) ---
    for source, plan in [('picset', picset_rd), ('ours', our_rd)]:
        if not plan:
            continue
        imgs = plan['images'] if 'images' in plan else plan.get('images', [])
        specs = plan.get('design_specs', '')
        img_path_out = f'{d}/{source}-img-1.png'
        if os.path.exists(img_path_out):
            print(f'  {source} img-1: cached', flush=True)
            continue
        if imgs:
            print(f'  {source} img-1: generating...', end=' ', flush=True)
            ok = generate_image(specs, imgs[0]['design_content'], ref_part, img_path_out)
            print('OK' if ok else 'FAIL', flush=True)
            time.sleep(3)

    # --- Score both ---
    picset_img = f'{d}/picset-img-1.png'
    our_img = f'{d}/ours-img-1.png'
    ref = img_path

    product_scores = {'product': pname, 'picset': -1, 'ours': -1}
    
    if os.path.exists(picset_img):
        print(f'  Scoring PicSet...', end=' ', flush=True)
        ps = score_image(ref, picset_img)
        product_scores['picset'] = ps['score']
        product_scores['picset_issues'] = ps.get('issues', [])
        print(f'{ps["score"]}', flush=True)
    
    if os.path.exists(our_img):
        print(f'  Scoring Ours...', end=' ', flush=True)
        os_ = score_image(ref, our_img)
        product_scores['ours'] = os_['score']
        product_scores['ours_issues'] = os_.get('issues', [])
        print(f'{os_["score"]}', flush=True)

    all_scores.append(product_scores)

# === SUMMARY ===
with open(f'{OUT_DIR}/scores.json', 'w', encoding='utf-8') as f:
    json.dump(all_scores, f, ensure_ascii=False, indent=2)

print(f'\n{"Product":<12} {"PicSet":<8} {"Ours":<8} {"Winner"}')
print('-' * 40)
pt = ot = n = 0
pw = ow = ties = 0
for r in all_scores:
    p, o = r['picset'], r['ours']
    if p < 0 or o < 0:
        continue
    w = 'PicSet' if p > o else ('Ours' if o > p else 'Tie')
    if p > o: pw += 1
    elif o > p: ow += 1
    else: ties += 1
    print(f'{r["product"]:<12} {p:<8} {o:<8} {w}')
    pt += p; ot += o; n += 1
print('-' * 40)
if n:
    print(f'{"Average":<12} {pt/n:<8.1f} {ot/n:<8.1f}')
    print(f'Wins: PicSet={pw} Ours={ow} Tie={ties}')
