# MercaFlow

AI e-commerce product photography pipeline, reverse-engineered from PicSet AI. Generates professional main images and detail image sets from a single product photo.

## Architecture

4-step pipeline (`pipeline/` directory):
- **Step 0** (`step0_ai_write.py`): AI generates 3 style options from product photo, auto-selects best one
- **Step 1** (`step1_analyze.py`): Analyzes product + generates design specs + per-image briefs (Chinese)
- **Step 2** (`step2_expand.py`): Converts Chinese briefs → structured English prompts (250-350 words, 11 elements)
- **Step 3** (`step3_generate.py`): Sends English prompt + reference photo → Gemini image generation

Run: `python -m pipeline.run <image> --type main|detail --count N --lang es|none|en --skip-generate`

## Key Files

- `vertex_client.py` — Multi-project round-robin client (3 GCP projects for rate limit mitigation)
- `pipeline/config.py` — Language map, defaults
- `pipeline/retry.py` — Exponential backoff for 429 errors (max_retries=5, base_delay=30s)
- `prompts/picset-*.txt` — Reverse-engineered prompt templates from PicSet AI
- `.pi-handoff/PICSET_COMPLETE_REVERSE_ENGINEERING.md` — Full reverse engineering report

## Vertex AI Setup

- 3 GCP projects rotating: `project-a1331a0f-a61c-4d85-adb`, `project-7e9a15c4-687c-4500-917`, `mercaflow-pool-2`
- Auth: Application Default Credentials (`gcloud auth application-default login`)
- Models: `gemini-3-flash-preview` (text planning), `gemini-3-pro-image-preview` (image generation)
- Location: `global` (preview models only available on global endpoint)
- Rate limits: 2 RPM image gen per project (hard limit), ~10 RPM text gen

## Conventions

- All code comments and git messages in English
- User communication in Chinese
- Generated prompts must be pure English (except target language text content like Spanish copywriting)
- Step 3 uses system_instruction for product fidelity rules
- Main images vs detail images use different analysis templates but same generator template

## Quick Commands

```bash
# Full pipeline (skip image gen for testing)
python -m pipeline.run test-products/stationery/product-10.jpg --type main --count 4 --lang es --skip-generate

# Generate images from saved prompts
python -m pipeline.step3_generate <ref_image> <step2_expanded.json> <output_dir>

# Single image retry
python -c "from pipeline.step3_generate import generate_one; generate_one('ref.jpg', 'prompt text', 'out.png')"
```
