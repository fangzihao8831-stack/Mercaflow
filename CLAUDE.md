# MercaFlow

Two-part AI e-commerce system: image generation pipeline + MercadoLibre Mexico listing automation.

## Architecture

### Image Generation Pipeline (`pipeline/`)
4-step pipeline, reverse-engineered from PicSet AI:
- **Step 0** (`step0_ai_write.py`): AI generates 3 style options from product photo, auto-selects best one
- **Step 1** (`step1_analyze.py`): Analyzes product + generates design specs + per-image briefs (Chinese)
- **Step 2** (`step2_expand.py`): Converts Chinese briefs → structured English prompts (250-350 words, 11 elements)
- **Step 3** (`step3_generate.py`): Sends English prompt + reference photo → Gemini image generation

Run: `python -m pipeline.run <image> --type main|detail --count N --lang es|none|en --skip-generate`

### MeLi Listing Pipeline (`meli/`)
13-step orchestrator that takes product images + import cost → live MercadoLibre listing:
1. LLM quick scan → product name
2. `domain_discovery` → category candidates → LLM picks best fit
3. Fetch category attributes
4. Full LLM analysis → title, description, attributes (or skip if both overrides set)
5. Apply defaults, SKU, GTIN, package dims
6. `listing_prices` API → calculate price with commission
7. Build listing body
8. Upload images (dry_run stops here)
9. Validate listing
10. Create listing
11. Add description
12. Verify profit (commission + shipping + taxes)
13. Margin guard + auto-pause

Run: `python -m meli.orchestrator` (dry_run test with jewelry box)

## Key Files

### Image Generation
- `vertex_client.py` — Multi-project round-robin Vertex AI client
- `pipeline/config.py` — Language map, defaults
- `pipeline/retry.py` — Exponential backoff for 429 errors
- `prompts/picset-*.txt` — Reverse-engineered PicSet prompt templates

### MeLi Listing
- `meli/llm.py` — Provider-agnostic LLM layer (Vertex AI / Gemini API / OpenAI-compatible)
- `meli/analyze.py` — Product image analysis → listing content (title, description, attributes)
- `meli/orchestrator.py` — 13-step listing creation pipeline
- `meli/client.py` — MeLi API client with auth, rate limiting, retries (429 + 5xx)
- `meli/auth.py` — OAuth 2.0 flow + proactive token refresh
- `meli/costs.py` — Pricing calculator (commission + tax + shipping → sell price)
- `meli/listings.py` — Listing helpers
- `meli/cli.py` — CLI for testing MeLi API calls

## LLM Provider Setup (`meli/llm.py`)

Provider-agnostic — supports Vertex AI, Gemini API key, and any OpenAI-compatible endpoint.

```bash
# Vertex AI (default) — uses ADC auth
export LLM_PROVIDER=vertex
export VERTEX_PROJECT=project-a1331a0f-a61c-4d85-adb
export VERTEX_LOCATION=global
export LLM_MODEL=gemini-3-flash-preview

# Gemini Developer API — uses API key
export LLM_PROVIDER=gemini
export GEMINI_API_KEY=AIza...
export LLM_MODEL=gemini-2.0-flash

# OpenAI-compatible (MiniMax, DeepSeek, OpenAI, etc.)
export LLM_PROVIDER=openai
export OPENAI_API_KEY=xxx
export OPENAI_BASE_URL=https://api.minimax.chat/v1
export LLM_MODEL=minimax-m1
```

## Vertex AI Setup (Image Generation)

- 3 GCP projects rotating: `project-a1331a0f-a61c-4d85-adb`, `project-7e9a15c4-687c-4500-917`, `mercaflow-pool-2`
- Auth: Application Default Credentials (`gcloud auth application-default login`)
- Models: `gemini-3-flash-preview` (text), `gemini-3-pro-image-preview` (image gen)
- Location: `global` (preview models only available on global endpoint)
- Rate limits: 2 RPM image gen per project (hard limit), ~10 RPM text gen

## MeLi API Setup

- Site: MLM (Mexico only), currency MXN
- Auth: OAuth 2.0 via `python -m meli.auth` → tokens saved to `meli/.tokens.json`
- Access token: 6h life, auto-refreshes. Proactive refresh at pipeline start if <1h remaining.
- Commission: ~15% Clásica, ~19% Premium (via `listing_prices` API)
- Tax formula: `tax_base = price / 1.16; taxes = tax_base * 0.105` (~9.05% effective)
- Free shipping: forced by MeLi when price ≥ $299 MXN

## Conventions

- All code comments and git messages in English
- User communication in Chinese
- Generated prompts must be pure English (except target language text content like Spanish copywriting)
- Mexico-only: no multi-country logic in meli/

## Quick Commands

```bash
# Image pipeline (skip image gen for testing)
python -m pipeline.run test-products/stationery/product-10.jpg --type main --count 4 --lang es --skip-generate

# MeLi orchestrator dry run
python -m meli.orchestrator

# MeLi auth setup
python -m meli.auth

# MeLi CLI (inspect items, test API)
python -m meli.cli item MLM2843240761
python -m meli.cli list
```
