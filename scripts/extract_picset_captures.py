"""Extract PicSet pipeline — v2 with correct field paths.

Fields used:
- postData = request body (not 'reqBody')
- respBody = response body
- payload.ai_request = the leaked server-side prompt (nested!)
- result_data = the leaked server-side response
"""
import json
import re
from pathlib import Path
from collections import defaultdict

BASE = Path(r'C:\Users\fangz\OneDrive\Desktop\MercaFlow')
CAPS = [BASE / 'evals' / 'picset-capture.json', BASE / 'evals' / 'picset-capture-2.json']
OUT = BASE / '.pi-handoff' / 'picset_pipeline_extracted.md'


def load_all():
    records = []
    for fp in CAPS:
        if not fp.exists():
            continue
        with fp.open(encoding='utf-8') as f:
            data = json.load(f)
        for i, r in enumerate(data):
            r['_src'] = fp.name
            r['_idx'] = i
            records.append(r)
    return records


def short_url(url):
    return (url
            .replace('https://picsetai.cn/supabase', '<sb>')
            .replace('https://cdn.picsetai.cn', '<cdn>')
            .replace('https://oss-cn-shanghai.aliyuncs.com', '<oss>'))


def try_json(s):
    if not s:
        return None
    try:
        return json.loads(s)
    except Exception:
        return None


def trunc(s, n):
    if not isinstance(s, str):
        return s
    return s if len(s) <= n else s[:n] + f'... [+{len(s)-n}c]'


def main():
    records = load_all()

    # 1. Index by endpoint category
    by_endpoint = defaultdict(list)
    for r in records:
        u = r['url'].split('?')[0]
        # Keep only functions/v1/X and rest/v1/generation_jobs
        if 'functions/v1/' in u:
            name = u.rsplit('/', 1)[-1]
            by_endpoint[name].append(r)
        elif 'generation_jobs' in u:
            by_endpoint['generation_jobs'].append(r)
        elif 'projects' in u and 'rest/v1' in u:
            by_endpoint['projects'].append(r)

    # 2. Index generation_jobs by (job_id, type, status)
    jobs_by_type = defaultdict(list)  # type -> [success records]
    for r in by_endpoint['generation_jobs']:
        parsed = try_json(r.get('respBody'))
        if not isinstance(parsed, dict):
            continue
        if parsed.get('status') == 'success':
            jtype = parsed.get('type', 'UNKNOWN')
            jobs_by_type[jtype].append((r, parsed))

    lines = []
    lines.append('# PicSet Pipeline — Complete Extraction (v2)')
    lines.append('')
    lines.append(f'Source: {len(records)} total records from 2 capture files')
    lines.append('')

    # === Section 1: Endpoint inventory ===
    lines.append('## 1. PicSet Edge Functions Called')
    lines.append('')
    lines.append('| Endpoint | Calls |')
    lines.append('|---|---|')
    for name, rs in sorted(by_endpoint.items(), key=lambda x: -len(x[1])):
        if name == 'generation_jobs':
            lines.append(f'| `rest/v1/generation_jobs` (polling) | {len(rs)} |')
        elif name == 'projects':
            lines.append(f'| `rest/v1/projects` | {len(rs)} |')
        else:
            lines.append(f'| `functions/v1/{name}` | {len(rs)} |')
    lines.append('')

    # === Section 2: Completed jobs by type ===
    lines.append('## 2. Completed Jobs by Type')
    lines.append('')
    lines.append('| Type | Count |')
    lines.append('|---|---|')
    for t, rs in jobs_by_type.items():
        lines.append(f'| `{t}` | {len(rs)} |')
    lines.append('')

    # === Section 3: Edge function requests ===
    lines.append('## 3. Edge Function Requests (what the client sends)')
    lines.append('')

    for name in ['ai-write-requirements', 'analyze-product-v2', 'generate-prompts-v2', 'generate-image', 'ai-write-quota', 'get-oss-sts']:
        if name not in by_endpoint:
            continue
        lines.append(f'### 3.{["ai-write-requirements","analyze-product-v2","generate-prompts-v2","generate-image","ai-write-quota","get-oss-sts"].index(name)+1} `functions/v1/{name}`')
        lines.append('')
        for i, r in enumerate(by_endpoint[name][:3], 1):
            lines.append(f'**Call {i}** (src=`{r["_src"]}`, status=`{r.get("status")}`)')
            lines.append('')
            pd = try_json(r.get('postData'))
            if pd:
                lines.append('Request body:')
                lines.append('```json')
                lines.append(json.dumps(pd, ensure_ascii=False, indent=2)[:4000])
                lines.append('```')
            lines.append('')
            # For non-SSE endpoints, also dump the response
            if name != 'generate-prompts-v2':
                rb = try_json(r.get('respBody'))
                if rb:
                    lines.append('Response body:')
                    lines.append('```json')
                    lines.append(json.dumps(rb, ensure_ascii=False, indent=2)[:1500])
                    lines.append('```')
                    lines.append('')
        lines.append('')

    # === Section 4: The leaked server-side prompts (via payload.ai_request) ===
    lines.append('## 4. Leaked Server-Side AI Requests')
    lines.append('')
    lines.append('PicSet stores the exact Gemini request in `payload.ai_request` of the `generation_jobs` row. This leaks when we poll the job row — giving us the EXACT prompt, model, config, and image references they send to Google.')
    lines.append('')

    seen_prompts = set()
    for jtype, entries in jobs_by_type.items():
        for record, parsed in entries:
            payload = parsed.get('payload', {})
            ai_req = payload.get('ai_request') if isinstance(payload, dict) else None
            if not ai_req:
                continue
            # Dedupe by the prompt text
            prompt_text = ''
            contents = ai_req.get('contents', [])
            if contents and isinstance(contents[0], dict):
                parts = contents[0].get('parts', [])
                for p in parts:
                    if isinstance(p, dict) and 'text' in p:
                        prompt_text = p['text']
                        break
            key = (jtype, prompt_text[:300])
            if key in seen_prompts:
                continue
            seen_prompts.add(key)

            lines.append(f'### 4.{len(seen_prompts)} `{jtype}` — model `{ai_req.get("model")}`, provider `{ai_req.get("provider")}`')
            lines.append('')

            cfg = ai_req.get('generationConfig', {})
            lines.append(f'**Config**: `temperature={cfg.get("temperature")}`, `maxOutputTokens={cfg.get("maxOutputTokens")}`, `responseMimeType={cfg.get("responseMimeType")}`')
            lines.append('')

            # Job-level metadata
            pm = parsed.get('provider_meta', {})
            lines.append(f'**Provider meta**: source=`{pm.get("source")}`, target_language=`{pm.get("target_language")}`, image_count=`{pm.get("image_count")}`')
            lines.append(f'**Job fields**: gen_model=`{parsed.get("gen_model")}`, gen_resolution=`{parsed.get("gen_resolution")}`, gen_family=`{parsed.get("gen_family")}`, speed_mode=`{parsed.get("speed_mode")}`, workflow_mode=`{parsed.get("workflow_mode")}`')
            if payload.get('promptConfigKey'):
                lines.append(f'**Prompt config key**: `{payload["promptConfigKey"]}`')
            lines.append('')

            lines.append('**System prompt / first text part**:')
            lines.append('```')
            lines.append(trunc(prompt_text, 8000))
            lines.append('```')
            lines.append('')

            # Show the other parts (images, follow-up text)
            other_parts = []
            for p in parts[1:]:  # skip first text
                if isinstance(p, dict):
                    if 'text' in p:
                        other_parts.append(f"TEXT: {trunc(p['text'], 500)}")
                    elif 'inlineData' in p or 'inline_data' in p:
                        inline = p.get('inlineData') or p.get('inline_data', {})
                        data_ref = inline.get('data', '')
                        mime = inline.get('mimeType') or inline.get('mime_type', '')
                        # Data can be URL or base64
                        if isinstance(data_ref, str) and data_ref.startswith('http'):
                            other_parts.append(f'IMAGE URL ({mime}): {data_ref}')
                        else:
                            other_parts.append(f'IMAGE base64 ({mime}, {len(data_ref) if isinstance(data_ref, str) else 0} chars)')

            if other_parts:
                lines.append('**Other parts in order**:')
                for op in other_parts:
                    lines.append(f'- {op}')
                lines.append('')

    # === Section 5: Job result_data (the actual Gemini responses) ===
    lines.append('## 5. Leaked Server-Side Responses (`result_data`)')
    lines.append('')
    lines.append('The Gemini response is stored in `result_data`. This is the full output that PicSet displays in the UI.')
    lines.append('')

    for jtype in ['AI_WRITE', 'ANALYSIS', 'IMAGE_GEN']:
        if jtype not in jobs_by_type:
            continue
        for record, parsed in jobs_by_type[jtype][:2]:
            payload = parsed.get('payload', {})
            result = parsed.get('result_data')
            if not result:
                continue
            lines.append(f'### 5.{jtype}')
            lines.append('')

            # For IMAGE_GEN, also dump the RAW payload which contains the English prompt sent
            if jtype == 'IMAGE_GEN' and isinstance(payload, dict):
                prompts_arr = payload.get('prompts') or payload.get('prompt') or []
                if prompts_arr:
                    lines.append('**Payload `prompts`** (this is the English expanded prompt from step 2):')
                    lines.append('```json')
                    lines.append(json.dumps(prompts_arr, ensure_ascii=False, indent=2)[:4000])
                    lines.append('```')
                    lines.append('')

            lines.append('**result_data**:')
            lines.append('```json')
            lines.append(json.dumps(result, ensure_ascii=False, indent=2)[:6000])
            lines.append('```')
            lines.append('')
            break  # one per type is enough

    # === Section 6: ANALYSIS payload (contains the requirements text, imageCount, language) ===
    lines.append('## 6. `ANALYSIS` Job Payload (client → server input for step 1)')
    lines.append('')

    for record, parsed in jobs_by_type.get('ANALYSIS', [])[:3]:
        payload = parsed.get('payload', {})
        lines.append(f'### {parsed.get("id", "?")[:8]}… — image_count=`{parsed.get("provider_meta", {}).get("image_count")}`, target_lang=`{parsed.get("provider_meta", {}).get("target_language")}`')
        lines.append('')
        lines.append('```json')
        # Strip ai_request from payload to keep it compact (shown in section 4)
        display = {k: v for k, v in payload.items() if k != 'ai_request'}
        lines.append(json.dumps(display, ensure_ascii=False, indent=2)[:3000])
        lines.append('```')
        lines.append('')

    # === Section 7: IMAGE_GEN full payload (shows what gets sent to the image model) ===
    lines.append('## 7. `IMAGE_GEN` Full Payload')
    lines.append('')

    for record, parsed in jobs_by_type.get('IMAGE_GEN', [])[:2]:
        payload = parsed.get('payload', {})
        lines.append(f'### Job `{parsed.get("id", "?")[:8]}…`')
        lines.append('')
        lines.append(f'Fields: `gen_model={parsed.get("gen_model")}`, `gen_resolution={parsed.get("gen_resolution")}`, `gen_family={parsed.get("gen_family")}`, `speed_mode={parsed.get("speed_mode")}`, `workflow_mode={parsed.get("workflow_mode")}`')
        lines.append('')
        lines.append('**Payload (excluding ai_request)**:')
        lines.append('```json')
        display = {k: v for k, v in payload.items() if k != 'ai_request'}
        lines.append(json.dumps(display, ensure_ascii=False, indent=2)[:5000])
        lines.append('```')
        lines.append('')

    # === Section 8: SSE stream reconstruction for generate-prompts-v2 ===
    lines.append('## 8. `generate-prompts-v2` SSE Streams (the HIDDEN step)')
    lines.append('')
    lines.append('This endpoint does not write a `generation_jobs` row with an `ai_request` field — it just streams SSE directly back. So we only see the OUTPUT (the expanded English prompts), not PicSet\'s server-side prompt that produced them. To get PicSet\'s expansion prompt, we would need prompt injection or bundled JS inspection.')
    lines.append('')

    sse_calls = [r for r in records if 'generate-prompts-v2' in r['url']]
    lines.append(f'{len(sse_calls)} SSE call(s) captured')
    lines.append('')

    for i, r in enumerate(sse_calls, 1):
        lines.append(f'### SSE Call {i} (src=`{r["_src"]}`)')
        lines.append('')

        # Show what was sent (postData)
        pd = try_json(r.get('postData'))
        if pd:
            lines.append('**Client → server request**:')
            lines.append('```json')
            lines.append(json.dumps(pd, ensure_ascii=False, indent=2)[:3000])
            lines.append('```')
            lines.append('')

        # Reconstruct SSE
        raw = r.get('respBody', '')
        if not raw:
            continue
        chunks = re.findall(r'data:\s*(\{[^\n]*\})', raw)
        if not chunks:
            continue

        last = chunks[-1]
        parsed = try_json(last)
        if parsed and 'fullText' in parsed:
            full = parsed['fullText']
            inner = try_json(full)
            if inner:
                lines.append(f'**Expanded prompts** ({len(inner)} image(s)):')
                lines.append('')
                for idx, item in enumerate(inner, 1):
                    lines.append(f'#### Image {idx}')
                    lines.append('')
                    prompt_val = item.get('prompt', '') if isinstance(item, dict) else str(item)
                    lines.append('```')
                    lines.append(trunc(prompt_val, 5000))
                    lines.append('```')
                    lines.append('')
            else:
                lines.append(f'_fullText parse failed, raw:_')
                lines.append('```')
                lines.append(trunc(full, 5000))
                lines.append('```')
                lines.append('')

    OUT.write_text('\n'.join(lines), encoding='utf-8')
    print(f'Wrote {OUT}')
    print(f'Size: {OUT.stat().st_size/1024:.1f} KB')
    print(f'Leaked prompts extracted: {len(seen_prompts)}')


if __name__ == '__main__':
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    main()
