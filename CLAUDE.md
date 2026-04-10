# MercaFlow

MercadoLibre Mexico listing automation. Takes product images + import cost → live listing with AI-generated title, description, attributes, and pricing.

Image generation pipeline has been extracted to a separate repo: `MercaPic/`

## Architecture

13-step orchestrator (`meli/orchestrator.py`):
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
- Mexico-only: no multi-country logic

## Quick Commands

```bash
# MeLi orchestrator dry run
python -m meli.orchestrator

# MeLi auth setup
python -m meli.auth

# MeLi CLI (inspect items, test API)
python -m meli.cli item MLM2843240761
python -m meli.cli list
```
