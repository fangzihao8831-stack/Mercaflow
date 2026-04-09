# -*- coding: utf-8 -*-
"""
MercaFlow — MercadoLibre API Client
Reusable wrapper with auth handling, rate limiting, retries, and convenience methods.
"""
import io
import sys
import time
import mimetypes
from pathlib import Path

import requests

# Windows UTF-8 stdout fix
if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from .auth import get_access_token, get_headers, refresh_token, load_tokens

API_BASE = "https://api.mercadolibre.com"
SITE_ID = "MLM"

MAX_RETRIES = 3
MULTIGET_BATCH = 20


class MeliAPIError(Exception):
    """Raised when MeLi API returns an error response."""

    def __init__(self, status_code: int, body: dict | str, endpoint: str = ""):
        self.status_code = status_code
        self.body = body
        self.endpoint = endpoint
        msg = f"MeLi API {status_code} on {endpoint}"
        if isinstance(body, dict):
            msg += f": {body.get('message', body.get('error', body))}"
        else:
            msg += f": {body}"
        super().__init__(msg)


class MeliClient:
    """MercadoLibre API client with auth, rate limiting, and retries."""

    def __init__(self):
        self.session = requests.Session()
        self._load_auth()

    # ------------------------------------------------------------------
    # Auth
    # ------------------------------------------------------------------

    def _load_auth(self):
        """Load current access token into session headers."""
        token = get_access_token()
        self.session.headers.update({
            "Authorization": f"Bearer {token}",
        })

    def _refresh_auth(self):
        """Force-refresh the token and update session headers."""
        tokens = load_tokens()
        if tokens:
            tokens = refresh_token(tokens)
            self.session.headers.update({
                "Authorization": f"Bearer {tokens['access_token']}",
            })
        else:
            # Fallback — get_access_token will exit if no tokens
            self._load_auth()

    # ------------------------------------------------------------------
    # Core HTTP
    # ------------------------------------------------------------------

    def _request(self, method: str, endpoint: str, **kwargs) -> dict | list:
        """
        Execute an HTTP request with retry on 429 and auto-refresh on 401.
        Returns parsed JSON body. Raises MeliAPIError on failure.
        """
        url = endpoint if endpoint.startswith("http") else f"{API_BASE}{endpoint}"

        for attempt in range(1, MAX_RETRIES + 1):
            resp = self.session.request(method, url, **kwargs)

            # Success
            if resp.status_code in (200, 201):
                return resp.json()

            # 204 No Content (some DELETEs)
            if resp.status_code == 204:
                return {}

            # 401 Unauthorized — refresh token once, then retry
            if resp.status_code == 401 and attempt == 1:
                print(f"  [meli] 401 on {endpoint}, refreshing token...")
                self._refresh_auth()
                continue

            # 429 Rate limited — wait and retry
            if resp.status_code == 429:
                retry_after = _parse_retry_after(resp)
                print(f"  [meli] 429 rate limited on {endpoint}, waiting {retry_after}s (attempt {attempt}/{MAX_RETRIES})")
                time.sleep(retry_after)
                continue

            # 5xx Server errors — retry with exponential backoff (1s / 2s / 4s)
            if 500 <= resp.status_code < 600 and attempt < MAX_RETRIES:
                wait = 2 ** (attempt - 1)
                print(f"  [meli] {resp.status_code} server error on {endpoint}, retrying in {wait}s (attempt {attempt}/{MAX_RETRIES})")
                time.sleep(wait)
                continue

            # Other errors — raise immediately
            try:
                body = resp.json()
            except Exception:
                body = resp.text
            raise MeliAPIError(resp.status_code, body, endpoint)

        # Exhausted retries
        try:
            body = resp.json()
        except Exception:
            body = resp.text
        raise MeliAPIError(resp.status_code, body, endpoint)

    def get(self, endpoint: str, params: dict | None = None) -> dict | list:
        """GET request with auth and retries."""
        return self._request("GET", endpoint, params=params)

    def post(self, endpoint: str, json: dict | None = None, data=None, files=None) -> dict | list:
        """POST request with auth and retries."""
        return self._request("POST", endpoint, json=json, data=data, files=files)

    def put(self, endpoint: str, json: dict | None = None) -> dict | list:
        """PUT request with auth and retries."""
        return self._request("PUT", endpoint, json=json)

    def delete(self, endpoint: str) -> dict:
        """DELETE request with auth and retries."""
        return self._request("DELETE", endpoint)

    # ------------------------------------------------------------------
    # User
    # ------------------------------------------------------------------

    def get_user(self) -> dict:
        """GET /users/me — current authenticated user."""
        return self.get("/users/me")

    # ------------------------------------------------------------------
    # Items
    # ------------------------------------------------------------------

    def get_item(self, item_id: str) -> dict:
        """GET /items/{id} — single item details."""
        return self.get(f"/items/{item_id}")

    def get_items(self, item_ids: list[str], attributes: str | None = None) -> list[dict]:
        """
        GET /items?ids=x,y,z — multiget in batches of 20.
        Returns flat list of item body dicts.
        """
        results = []
        for i in range(0, len(item_ids), MULTIGET_BATCH):
            batch = item_ids[i : i + MULTIGET_BATCH]
            params = {"ids": ",".join(batch)}
            if attributes:
                params["attributes"] = attributes
            resp = self.get("/items", params=params)
            for entry in resp:
                if entry.get("code") == 200:
                    results.append(entry["body"])
                else:
                    results.append(entry)
        return results

    def search_items(self, user_id: str | None = None, **params) -> dict:
        """
        GET /users/{user_id}/items/search
        If user_id is None, fetches it from /users/me.
        """
        if user_id is None:
            user_id = str(self.get_user()["id"])
        return self.get(f"/users/{user_id}/items/search", params=params or None)

    def create_item(self, item_data: dict) -> dict:
        """POST /items — create a new listing."""
        return self.post("/items", json=item_data)

    def validate_item(self, item_data: dict) -> dict:
        """POST /items/validate — validate listing data without creating."""
        return self.post("/items/validate", json=item_data)

    def update_item(self, item_id: str, data: dict) -> dict:
        """PUT /items/{id} — update an existing listing."""
        return self.put(f"/items/{item_id}", json=data)

    def add_description(self, item_id: str, plain_text: str) -> dict:
        """POST /items/{id}/description — add plain text description."""
        return self.post(f"/items/{item_id}/description", json={"plain_text": plain_text})

    # ------------------------------------------------------------------
    # Images
    # ------------------------------------------------------------------

    def upload_image(self, image_path: str | Path) -> dict:
        """
        POST /pictures/items/upload — upload image for listing.
        Returns dict with 'id' (e.g. '984371-MLM12345_1') and 'variations' urls.
        """
        image_path = Path(image_path)
        if not image_path.exists():
            raise FileNotFoundError(f"Image not found: {image_path}")

        mime, _ = mimetypes.guess_type(str(image_path))
        mime = mime or "image/jpeg"

        with open(image_path, "rb") as f:
            # For file uploads, don't send Content-Type in session headers —
            # let requests set multipart boundary automatically.
            files = {"file": (image_path.name, f, mime)}
            return self.post("/pictures/items/upload", files=files)

    # ------------------------------------------------------------------
    # Categories
    # ------------------------------------------------------------------

    def get_category(self, category_id: str) -> dict:
        """GET /categories/{id} — category details."""
        return self.get(f"/categories/{category_id}")

    def get_category_attributes(self, category_id: str) -> list[dict]:
        """GET /categories/{id}/attributes — required/optional attributes."""
        return self.get(f"/categories/{category_id}/attributes")

    def predict_category(self, title: str) -> dict:
        """GET /sites/MLM/category_predictor/predict?title=... — predict category from title."""
        return self.get(f"/sites/{SITE_ID}/category_predictor/predict", params={"title": title})

    # ------------------------------------------------------------------
    # Pricing & Shipping
    # ------------------------------------------------------------------

    def get_listing_prices(
        self,
        price: float,
        category_id: str | None = None,
        listing_type_id: str | None = None,
    ) -> dict:
        """GET /sites/MLM/listing_prices — fee breakdown for a price point."""
        params = {"price": price}
        if category_id:
            params["category_id"] = category_id
        if listing_type_id:
            params["listing_type_id"] = listing_type_id
        return self.get(f"/sites/{SITE_ID}/listing_prices", params=params)

    def get_shipping_options(self, item_id: str, zip_code: str) -> dict:
        """GET /items/{id}/shipping_options?zip_code=... — available shipping methods."""
        return self.get(f"/items/{item_id}/shipping_options", params={"zip_code": zip_code})

    # ------------------------------------------------------------------
    # Trends & Search
    # ------------------------------------------------------------------

    def get_trends(self) -> list[dict]:
        """GET /trends/MLM — trending searches."""
        return self.get(f"/trends/{SITE_ID}")

    def search_products(
        self,
        query: str | None = None,
        product_identifier: str | None = None,
    ) -> dict:
        """GET /products/search?site_id=MLM — search product catalog."""
        params = {"site_id": SITE_ID}
        if query:
            params["q"] = query
        if product_identifier:
            params["product_identifier"] = product_identifier
        return self.get("/products/search", params=params)

    # ------------------------------------------------------------------
    # Analytics
    # ------------------------------------------------------------------

    def get_item_visits(self, item_id: str) -> dict:
        """GET /items/{id}/visits — visit count."""
        return self.get(f"/items/{item_id}/visits")

    def get_item_performance(self, item_id: str) -> dict:
        """GET /item/{id}/performance — listing health/performance metrics."""
        return self.get(f"/item/{item_id}/performance")


# ----------------------------------------------------------------------
# Helpers
# ----------------------------------------------------------------------

def _parse_retry_after(resp: requests.Response) -> float:
    """Extract retry delay from 429 response. Defaults to 2s."""
    # MeLi sometimes sends Retry-After header
    retry_after = resp.headers.get("Retry-After")
    if retry_after:
        try:
            return max(float(retry_after), 0.5)
        except ValueError:
            pass
    # Fallback: check X-RateLimit-Reset or default
    return 2.0


# ----------------------------------------------------------------------
# CLI smoke test
# ----------------------------------------------------------------------

if __name__ == "__main__":
    print("\n  MercaFlow — MeLi API Client Test\n")
    client = MeliClient()

    user = client.get_user()
    print(f"  User: {user['nickname']} (ID: {user['id']})")

    items = client.search_items(limit=5)
    total = items.get("paging", {}).get("total", 0)
    print(f"  Items: {total} total")

    if items.get("results"):
        first = client.get_item(items["results"][0])
        print(f"  First item: {first.get('title', '?')} — ${first.get('price', 0):,.2f}")

    print("\n  [OK] Client working.\n")
