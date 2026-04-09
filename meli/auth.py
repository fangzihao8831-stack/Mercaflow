# -*- coding: utf-8 -*-
"""
MercaFlow — MercadoLibre Auth CLI
Handles OAuth 2.0 flow: authorize, get tokens, auto-refresh, save/load tokens.
"""
import os
import sys
import json
import time
import webbrowser
import requests
from pathlib import Path
from dotenv import load_dotenv

# Load .env from project root
ENV_PATH = Path(__file__).parent.parent / ".env"
load_dotenv(ENV_PATH)

TOKEN_FILE = Path(__file__).parent / ".tokens.json"

APP_ID = os.environ.get("MELI_APP_ID")
CLIENT_SECRET = os.environ.get("MELI_CLIENT_SECRET")
REDIRECT_URI = os.environ.get("MELI_REDIRECT_URI", "https://www.google.com")

API_BASE = "https://api.mercadolibre.com"
AUTH_URL = "https://auth.mercadolibre.com.mx/authorization"


def save_tokens(data: dict):
    """Save tokens to file."""
    data["saved_at"] = int(time.time())
    with open(TOKEN_FILE, "w") as f:
        json.dump(data, f, indent=2)
    print(f"  Tokens saved to {TOKEN_FILE}")


def load_tokens() -> dict | None:
    """Load tokens from file."""
    if TOKEN_FILE.exists():
        with open(TOKEN_FILE) as f:
            return json.load(f)
    return None


def is_token_expired(tokens: dict) -> bool:
    """Check if access token is expired or about to expire (1 min buffer)."""
    saved_at = tokens.get("saved_at", 0)
    expires_in = tokens.get("expires_in", 0)
    return time.time() > (saved_at + expires_in - 60)


def authorize():
    """Step 1: Open browser for user to authorize the app."""
    url = f"{AUTH_URL}?response_type=code&client_id={APP_ID}&redirect_uri={REDIRECT_URI}"
    print(f"\n  Opening browser for authorization...")
    print(f"  URL: {url}\n")
    webbrowser.open(url)
    print("  After authorizing, you'll be redirected to Google.")
    print("  Copy the 'code' parameter from the URL bar.\n")
    print("  Example: https://www.google.com?code=TG-xxxxx-xxxxx\n")
    code = input("  Paste the code here: ").strip()
    return code


def exchange_code(code: str) -> dict:
    """Step 2: Exchange authorization code for access + refresh tokens."""
    resp = requests.post(f"{API_BASE}/oauth/token", json={
        "grant_type": "authorization_code",
        "client_id": APP_ID,
        "client_secret": CLIENT_SECRET,
        "code": code,
        "redirect_uri": REDIRECT_URI,
    })
    if resp.status_code != 200:
        print(f"  ERROR: {resp.status_code} — {resp.text}")
        sys.exit(1)
    data = resp.json()
    save_tokens(data)
    print(f"  Access token obtained! User ID: {data.get('user_id')}")
    print(f"  Expires in: {data.get('expires_in', 0) // 3600}h")
    return data


def refresh_token(tokens: dict) -> dict:
    """Refresh expired access token using refresh token."""
    resp = requests.post(f"{API_BASE}/oauth/token", json={
        "grant_type": "refresh_token",
        "client_id": APP_ID,
        "client_secret": CLIENT_SECRET,
        "refresh_token": tokens["refresh_token"],
    })
    if resp.status_code != 200:
        print(f"  Refresh failed: {resp.status_code} — {resp.text}")
        print("  You need to re-authorize. Run: python meli/auth.py")
        sys.exit(1)
    data = resp.json()
    save_tokens(data)
    print(f"  Token refreshed! Expires in: {data.get('expires_in', 0) // 3600}h")
    return data


def get_access_token() -> str:
    """Get a valid access token. Auto-refreshes if expired."""
    tokens = load_tokens()
    if not tokens:
        print("  No tokens found. Run: python meli/auth.py")
        sys.exit(1)
    if is_token_expired(tokens):
        print("  Token expired, refreshing...")
        tokens = refresh_token(tokens)
    return tokens["access_token"]


def ensure_fresh_token(min_remaining_seconds: int = 3600) -> str:
    """
    Ensure the access token has at least `min_remaining_seconds` of life left.
    Proactively refreshes if not. Returns the (possibly new) access token.

    Use this at the start of long pipelines to avoid mid-run expiration.
    Raises RuntimeError on failure (does NOT call sys.exit, unlike refresh_token).
    """
    tokens = load_tokens()
    if not tokens:
        raise RuntimeError("No MeLi tokens found. Run: python -m meli.auth")

    saved_at = tokens.get("saved_at", 0)
    expires_in = tokens.get("expires_in", 0)
    remaining = (saved_at + expires_in) - time.time()

    if remaining >= min_remaining_seconds:
        return tokens["access_token"]

    print(f"  Token has {int(remaining)}s remaining (< {min_remaining_seconds}s), refreshing proactively...")
    resp = requests.post(f"{API_BASE}/oauth/token", json={
        "grant_type": "refresh_token",
        "client_id": APP_ID,
        "client_secret": CLIENT_SECRET,
        "refresh_token": tokens["refresh_token"],
    })
    if resp.status_code != 200:
        raise RuntimeError(
            f"Token refresh failed ({resp.status_code}): {resp.text[:200]}. "
            f"Run: python -m meli.auth"
        )

    data = resp.json()
    save_tokens(data)
    print(f"  Token refreshed! Expires in: {data.get('expires_in', 0) // 3600}h")
    return data["access_token"]


def get_headers() -> dict:
    """Get auth headers for API calls."""
    return {"Authorization": f"Bearer {get_access_token()}"}


def test_auth():
    """Test authentication by fetching user info."""
    headers = get_headers()
    resp = requests.get(f"{API_BASE}/users/me", headers=headers)
    if resp.status_code != 200:
        print(f"  Auth test failed: {resp.status_code} — {resp.text}")
        return None
    user = resp.json()
    print(f"\n  [OK] Authenticated!")
    print(f"  User ID:    {user['id']}")
    print(f"  Nickname:   {user['nickname']}")
    print(f"  Country:    {user.get('country_id', '?')}")
    print(f"  Permalink:  {user.get('permalink', '?')}")
    return user


def list_items():
    """List all items for the authenticated seller."""
    headers = get_headers()
    
    # First get user ID
    user_resp = requests.get(f"{API_BASE}/users/me", headers=headers)
    if user_resp.status_code != 200:
        print(f"  Failed to get user: {user_resp.status_code}")
        return
    user_id = user_resp.json()["id"]
    
    # Search items
    resp = requests.get(
        f"{API_BASE}/users/{user_id}/items/search",
        headers=headers,
        params={"limit": 50}
    )
    if resp.status_code != 200:
        print(f"  Failed to list items: {resp.status_code} — {resp.text}")
        return
    
    data = resp.json()
    item_ids = data.get("results", [])
    total = data.get("paging", {}).get("total", 0)
    print(f"\n  Found {total} item(s)\n")
    
    if not item_ids:
        return
    
    # Fetch item details (multiget up to 20)
    ids_str = ",".join(item_ids[:20])
    items_resp = requests.get(
        f"{API_BASE}/items",
        headers=headers,
        params={"ids": ids_str, "attributes": "id,title,price,currency_id,status,available_quantity,sold_quantity,permalink,thumbnail,category_id,listing_type_id"}
    )
    
    if items_resp.status_code != 200:
        print(f"  Failed to fetch items: {items_resp.status_code}")
        return
    
    for item_data in items_resp.json():
        item = item_data.get("body", {})
        status_icon = "[ACTIVE]" if item.get("status") == "active" else "[INACTIVE]"
        print(f"  {status_icon} {item.get('id', '?')}")
        print(f"     Title:    {item.get('title', '?')}")
        print(f"     Price:    ${item.get('price', 0):,.2f} {item.get('currency_id', '')}")
        print(f"     Status:   {item.get('status', '?')}")
        print(f"     Stock:    {item.get('available_quantity', 0)} available, {item.get('sold_quantity', 0)} sold")
        print(f"     Type:     {item.get('listing_type_id', '?')}")
        print(f"     Category: {item.get('category_id', '?')}")
        print(f"     Link:     {item.get('permalink', '?')}")
        print()


if __name__ == "__main__":
    print("\n  MercaFlow — MercadoLibre Auth\n")
    
    if not APP_ID or not CLIENT_SECRET:
        print("  ERROR: MELI_APP_ID and MELI_CLIENT_SECRET must be set in .env")
        sys.exit(1)
    
    tokens = load_tokens()
    
    if tokens and not is_token_expired(tokens):
        print("  Existing valid token found.")
        action = input("  [T]est auth / [L]ist items / [R]e-authorize? ").strip().lower()
    else:
        if tokens:
            print("  Token expired. Trying refresh...")
            try:
                tokens = refresh_token(tokens)
                action = input("  [T]est auth / [L]ist items? ").strip().lower()
            except SystemExit:
                action = "a"
        else:
            action = "a"
    
    if action == "a" or action == "r":
        code = authorize()
        tokens = exchange_code(code)
        test_auth()
    elif action == "l":
        list_items()
    else:
        test_auth()
