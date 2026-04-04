# MercaFlow

## What This Project Is
Automated e-commerce product photography and listing pipeline for MercadoLibre Mexico. Takes supplier catalog photos → generates professional listing images → creates listings with descriptions/pricing → uploads via MeLi API. Reverse-engineered from PicSet AI (picsetai.cn).

## Rules — Always Follow These
- **All image generation prompts must be in Chinese** — matches Gemini's training data for e-commerce
- **Use PicSet's exact prompt template** from `prompts/analysis-prompt.txt` — never write custom prompts
- **Use `response_mime_type="application/json"`** for all planning calls — eliminates parsing failures
- **One prompt file, one source of truth** — never hardcode prompts in scripts
- **Use Vertex AI endpoints** (`aiplatform.googleapis.com`) — NOT Gemini Developer API (disabled)
- **API keys live in `.env`** — never put secrets in this file or scripts
- **Use Chinese terminology**: 详情图要求, 整体设计规范, 图片规划, 产品复杂结构判定
- **Never create multiple pipeline scripts** — one clean `pipeline.py`, iterate on it
- **Every plan JSON must include metadata** (model, temperature, requirements, timestamp)
- **Evaluator prompt lives in `prompts/evaluator-prompt.txt`** — strict physical property checking

## Architecture

### Image Generation Pipeline (PicSet Clone)
```
Input: product photo + 详情图要求
        ↓
Gemini Flash (planning) → 整体设计规范 + 图片规划 (structured JSON)
        ↓
Gemini Pro (generation) → images (parallel, 30 workers max)
        ↓
Claude (validation) → structural hallucination check using evaluator prompt
```

### Planning Step
- Model: `gemini-3-flash-preview` via Vertex AI
- Params: `temperature=0.4`, `max_output_tokens=8192/16384`, `response_mime_type="application/json"`
- Prompt: `prompts/analysis-prompt.txt` with placeholders `{IMAGE_COUNT}`, `{TARGET_LANGUAGE}`, `{REQUIREMENTS}`
- Output: `{is_complex_product, design_specs, images[]}`

### Generation Step
- Model: `gemini-3-pro-image-preview` via Vertex AI
- `system_instruction` = `design_specs` (整体设计规范) + strict instruction
- `contents` = [reference photo(s), individual `design_content` (图片规划)]
- `image_size="2K"`, `aspect_ratio="1:1"`
- Use ThreadPoolExecutor for parallel generation

### Validation Step
- Model: Claude (via Anthropic OAuth)
- Prompt: `prompts/evaluator-prompt.txt`
- Checks physical properties (thickness, binding, material), structural integrity, product identity
- OAuth requires: `Authorization: Bearer {key}`, headers `anthropic-beta: claude-code-20250219,oauth-2025-04-20`, system block `"You are Claude Code, Anthropic's official CLI for Claude."`

## API Configuration
- All keys in `.env` file — load with `dotenv` or manual read
- **Vertex AI**: authenticate via `gcloud auth print-access-token`, NOT API key
- **Gemini Developer API**: DISABLED on project (per Google Support)
- **Anthropic OAuth**: token expires, refresh from `.pi/agent/auth.json`
- **PicSet**: anon key is permanent, access token expires (refresh from browser localStorage)
- Google Cloud Project: see `.env` for project ID

## Billing Status
- Billing account suspended — refund in progress (3-5 business days, Case #69012899)
- €242.60 Free Trial credit covers Vertex AI (including image generation)
- €848.21 GenAI App Builder credit covers Vertex AI Search ONLY
- Gemini Developer API NOT covered by any credits (policy since March 2, 2026)
- Must re-link billing to project after refund completes

## Business Context
- Import from AOSHIDA (usstore.tooerp.com/AOSHIDA) → brother's warehouse → Mercado FULL
- Active MeLi seller account (DAJIBA), User Products unlocked
- Currently <5 listings, no AI-generated images uploaded yet
- Multi-platform vision: MeLi → TikTok, Shein, Amazon
- Potential SaaS/ERP if pipeline works

## MeLi Catálogo (Grey Area)
- Catalog products have parent-child hierarchy (parent = generic, children = specific variants)
- Parent-child grouping is controlled by MeLi internally — NO seller API to force it
- PARENT_PK attributes (Brand, Model, Domain) must match for grouping
- CHILD_PK attributes (Color, Size) can differ
- "Crear productos" at `mercadolibre.com.mx/catalogo/sugerencias` — internal API: `POST /catalogo/api/suggestion`
- Catalog title max: 200 chars, description max: 50,000 chars
- User Products and Catalog are separate systems — catalog items don't get UP tags
- Strategy: submit multiple suggestions with same PARENT_PK, different CHILD_PK, hope MeLi groups them

## PicSet Reverse Engineering
- Analysis endpoint: `POST https://picsetai.cn/supabase/functions/v1/analyze-product-v2`
- Upload: Alibaba Cloud OSS via STS from `POST .../functions/v1/get-oss-sts`
- They use `gemini-3-flash-preview` with `temperature=0.4`, `responseMimeType=application/json`
- Analysis is FREE (0 credits), generation costs 5 credits/image
- Their prompt is our prompt — `prompts/analysis-prompt.txt` is PicSet's exact template

## Key Files
```
MercaFlow/
├── AGENTS.md                          ← this file
├── .env                               ← API keys (DO NOT COMMIT)
├── README.md                          ← project overview
├── prompts/
│   ├── analysis-prompt.txt            ← PicSet's exact planning prompt
│   └── evaluator-prompt.txt           ← strict physical property evaluator
├── generate-all-parallel.py           ← parallel image generation (30 workers)
├── run-comparison-v2.py               ← PicSet vs Ours comparison pipeline
├── evals/
│   ├── comparison-v2/                 ← 144 images + scores (9 products × 8 imgs × 2 sources)
│   ├── hallucinations-v2/             ← flagged hallucination images + references
│   └── laundry-basket-test/           ← original test from previous session
├── test-products/stationery/          ← 10 supplier catalog images
├── docs/                              ← 17 crawled MeLi developer docs
└── archive/                           ← old scripts and outputs
```

## Known Issues & Patterns
- **#1 hallucination**: Gemini Pro turns thin booklets/pamphlets into thick hardcover books — it invents thickness from flat 2D catalog images
- **Images 6-8 tend to fail** when requesting 8 images — model exhausts distinct shot ideas and starts inventing products
- **Catalog images cause more hallucinations than camera photos** — the laundry basket (3 WhatsApp photos) scored much better than stationery (1 catalog image each)
- **Interior colors bleed** if not explicitly stated in the planning prompt (e.g., jewelry box interior was pink instead of white)

## Full Workflow Vision (10 Steps)
1. 产品获取 — Scrape/select products from supplier (tooerp.com/AOSHIDA)
2. 产品分析 — Gemini Flash analyzes catalog image → 详情图要求
3. 图片规划 — Gemini Flash generates 整体设计规范 + 图片规划
4. 图片生成 — Gemini Pro generates images (parallel)
5. 质量验证 — Structural hallucination check against planning output
6. 重试循环 — Regenerate failed images with corrected prompts
7. 内容生成 — Spanish title, description, attributes for MeLi
8. 定价策略 — Import cost + MeLi commission + margin calculation
9. MeLi上架 — API upload: images + content + price + category
10. 目录管理 — Catálogo creation/joining + variant grouping

## Variant Handling (Not Built Yet)
- Catalog images often show multiple color variants in one photo
- Strategy: detect N variants → assign images per variant + common shots
- Example: 3 colors × 2 images each + 1 detail + 1 multi-color lineup = 8 total
- Primary variant dominates the set, multi-color shot gets exactly 1 image
- Other variants never appear as main subject unless seller requests it

## What's Built
- [x] PicSet's exact prompt template
- [x] Planning: Gemini Flash with structured JSON output
- [x] Generation: Gemini Pro with parallel workers (30 workers, 150 RPM)
- [x] PicSet API integration (upload, analyze, poll — direct HTTP)
- [x] Comparison pipeline: PicSet vs Ours across 10 products
- [x] 144 generated images scored with evaluator v2
- [x] Strict evaluator checking physical properties
- [x] Browser automation for PicSet and Google Cloud
- [x] MeLi developer docs crawled (17 docs)
- [x] MeLi catálogo internal API intercepted

## UI & API (In Progress)
- **UI**: Vite + React + TypeScript + Tailwind at `ui/` — run with `cd ui && npm run dev` (localhost:5173)
- **UI STATUS**: Fresh Vite install with tailwindcss and lucide-react. App.tsx needs to be built from scratch — the full design spec is in `docs/ui-design.md`. Key features to implement: image upload, image count slider, model/ratio/resolution/language dropdowns, variant chips, design specs viewer, shot brief cards, generated image grid with scores, advanced settings, status bar. Match PicSet's clean 2-column layout.
- **API**: FastAPI backend at `api/server.py` — run with `python -m uvicorn api.server:app --port 8000 --reload`
- **UI Design doc**: `docs/ui-design.md` — full wireframe and component hierarchy
- UI has: image upload, image count slider (3-10), model selector (NB Pro/NB 2/NB), aspect ratio, resolution, language, advanced settings (planning model, temperature, variant detection, auto-retry, parallel workers)
- All mock data for now — real Vertex AI calls wired up when billing returns
- WebSocket endpoint `/ws/generate` for real-time image streaming
- **ui-ux-pro-max-skill** installed at `.pi/skills/` for design intelligence

## PicSet UI Reference (what to match/improve)
- 2-column layout: left panel (input/settings), right panel (preview/results)
- Step indicator at top: 输入 → 分析中 → 确认规划 → 生成中 → 完成
- Left panel: image upload (0/6), 详情图要求 textarea (WE SKIP THIS - auto from photo), target language dropdown, model selector, aspect ratio, resolution, image count, speed mode (标准/快速/极速)
- Right panel: 整体设计规范 (collapsible, editable), 图片规划 cards (each with title, description, expand to see full brief, edit/delete buttons), generated images grid
- Clean white/gray design, rounded cards, blue primary color, minimal shadows
- Each 图片规划 card: number badge, title, short description, chevron to expand full design_content
- "Crear producto" button is blue, full width, shows credit cost
- Settings are in a compact 2×2 grid layout
- PicSet URL: picsetai.cn/studio-genesis

## Prompt Placeholders (analysis-prompt.txt)
- `{IMAGE_COUNT}` → UI slider (3-10), controls how many 图片规划 are generated
- `{TARGET_LANGUAGE}` → UI dropdown: "无文字(纯视觉)" / "中文" / "西班牙语(墨西哥)" / "英语" / "葡萄牙语(巴西)"
- `{REQUIREMENTS}` → auto-generated "无文案纯视觉设计，目标平台MercadoLibre拉丁美洲市场" + optional user notes
- Everything else (model, ratio, resolution, temperature) = API params, NOT prompt placeholders

## Comparison Results Summary
- 144 images generated (9 products × 8 images × 2 sources: PicSet vs Ours)
- With identical PicSet prompt: PicSet 77.3 avg vs Ours 74.9 avg (evaluator v2, strict)
- Both hallucinate at similar rates — PicSet 5 failures, Ours 8 failures
- #1 pattern: thin booklets rendered as thick books (images 6-8 worst)
- Evaluator v1 was too generous (scored 95 for wrong thickness), v2 catches physical properties
- Flash = Pro for planning quality (same output, 2.5x faster, confirmed across 6 products)

## Session History
- Previous session (deleted March 31): built laundry basket pipeline, 30 images caused 413 error
- This session (March 31 - April 3): rebuilt everything, reverse-engineered PicSet, comparison pipeline, evaluator v2, billing crisis, MeLi docs research, UI build
- Google billing: refund pending 3-5 days, must use Vertex AI (not Gemini Developer API), Generative Language API disabled on project

## What's NOT Built
- [ ] Vertex AI migration (code changes for new endpoints)
- [ ] Catalog image preprocessing (variant detection, crop)
- [ ] Per-variant shot planning
- [ ] Automated retry loop with prompt correction
- [ ] Spanish listing content generation (title, description, attributes)
- [ ] Pricing calculator (import cost + MeLi commissions + taxes + margin)
- [ ] MeLi API upload pipeline (item creation, image upload, catalog)
- [ ] MeLi catálogo automation (create products, submit for approval)
- [ ] Web UI
- [ ] Multi-platform support (TikTok, Shein, Amazon)
- [ ] Consolidated single `pipeline.py`
- [ ] Autonomous prompt improvement loop (eval-driven optimization)
