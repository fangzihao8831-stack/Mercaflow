# MercaFlow — AI E-Commerce Product Photography Pipeline

## What It Does
Takes a supplier catalog photo + product description → generates professional e-commerce listing images for MercadoLibre (Latin America).

## Architecture
Reverse-engineered from PicSet AI (picsetai.cn), adapted with our own improvements.

### Pipeline Steps
1. **Planning** — LLM analyzes product photo + user requirements → outputs `design_specs` (shared visual standard) + per-image `design_content` (shot briefs)
2. **Generation** — Gemini Nano Banana Pro generates images from ref photo + shot brief
3. **Evaluation** — Claude validates generated images against reference (optional)

### Key Technical Decisions
- **Planning model**: Gemini Flash (25s) or Claude Opus (92s) — both tested, Gemini Flash is faster + correctly identifies complex products
- **Generation model**: `gemini-3-pro-image-preview` (Nano Banana Pro), 2K, 1:1
- **Structured JSON output**: `response_mime_type="application/json"` — eliminates parsing step
- **PicSet's prompt template**: Fixed JSON schema with `[placeholder]` slots the LLM fills in
- **Complex product detection**: When true, locks product form/angles to reference only
- **All prompts in Chinese** — matches Gemini's training data for e-commerce imagery

## API Keys
- **Gemini**: see `.env` (Google Cloud trial)
- **Anthropic OAuth**: see `.env` (requires Bearer auth + `claude-code-20250219,oauth-2025-04-20` beta headers + Claude Code system prompt)

## Files

### Core Pipeline
- `pipeline-final.py` — Main script: runs both Gemini Flash and Claude Opus planning, generates 8 images each

### Key Documents
- `evals/picset-vs-mercaflow-analysis.md` — Detailed Chinese comparison of PicSet vs our pipeline
- `evals/picset-intercepted-api.json` — PicSet's actual API call (reverse-engineered)
- `evals/picset-run2-product08.md` — PicSet's exact prompts from their second run
- `MercadoLibre_Mexico_Image_Requirements.md` — MeLi photo rules research

### Test Products
- `test-products/stationery/product-08.jpg` — Jewelry box (main test product)
- `test-products/stationery/product-01..10.jpg` — 10 stationery products for future testing

### Generated Output Directories
- `test-products/stationery/final-gemini-plan/` — 8 images planned by Gemini Flash ⭐
- `test-products/stationery/final-claude-plan/` — 8 images planned by Claude Opus
- `evals/picset-prompts-our-gen/` — 5 images using PicSet's exact prompts on our Gemini
- `evals/laundry-basket-test/` — Original laundry basket test (from deleted session)
- Various `pipeline-v2..v5` output dirs (iteration history)

### Evaluator
- `evals/laundry-basket-test/evaluator-prompt-v5.md` — Customer-perspective validator (Chinese)
- `evals/laundry-basket-test/validator-prompt.md` — Single confidence_score validator (v3)
- `evals/laundry-basket-test/test-results.md` — Eval methodology findings

## PicSet's Prompt (Intercepted)
They use **one Gemini Flash call** per image with:
- `temperature: 0.4`
- `responseMimeType: "application/json"`
- `maxOutputTokens: 8192`
- A fixed prompt template with complex structure detection, view angle locking, and product form constraints
- `imageCount: 1` per call (not N images at once)

Their key innovation: **产品复杂结构判定** — when true:
1. View angles locked to reference photo only
2. Product shape/color/parts cannot be changed
3. Creative freedom limited to scene/lighting/props only

## Lessons Learned
1. **Structural audit > marketing copy** for product analysis
2. **Negative constraints** ("no mirror, no rivets") prevent hallucinations
3. **Product colors vs scene colors** must be separated
4. **Concrete nouns** ("三枚金色戒指") > abstract descriptions ("几枚精美首饰")
5. **`response_mime_type="application/json"`** eliminates parsing failures
6. **One planning call with forced JSON** beats multi-step Claude pipeline
7. **More reference photos = better fidelity** (laundry basket had 3, jewelry box had 1)
8. **Gemini Flash correctly identifies complex products**, Claude Opus didn't

## Next Steps
- [ ] Implement per-image planning calls (like PicSet) instead of all-at-once
- [ ] Add automated eval + retry loop
- [ ] Test on remaining 9 stationery products
- [ ] Build CLI interface (`python pipeline.py --refs photo.jpg --desc "..." --count 5`)
- [ ] Reference image preprocessing (strip catalog watermarks)
- [ ] Batch processing across multiple products
- [ ] MeLi compliance validation
