# -*- coding: utf-8 -*-
"""
MercaFlow — MercadoLibre Listing Management
Create, update, and manage MeLi listings via the API client.
"""
import sys
from pathlib import Path

# Windows UTF-8 stdout fix
if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from .client import MeliClient


# ------------------------------------------------------------------
# Listing Preparation
# ------------------------------------------------------------------

def prepare_listing(
    client: MeliClient,
    title: str,
    price: float,
    category_id: str | None = None,
    images: list[str] = [],
    description: str = "",
    attributes: dict = {},
    quantity: int = 1,
    condition: str = "new",
    listing_type: str = "gold_special",
) -> dict:
    """
    Build the item JSON body for POST /items.

    If category_id is None, uses client.predict_category(title) to auto-detect.
    Returns the full item body dict ready to submit to create_listing().
    """
    # Auto-detect category if not provided
    if category_id is None:
        print(f"  [listings] Predicting category for: {title}")
        prediction = client.predict_category(title)
        if isinstance(prediction, list) and prediction:
            category_id = prediction[0].get("id")
            cat_name = prediction[0].get("name", "?")
            print(f"  [listings] Predicted: {category_id} — {cat_name}")
        elif isinstance(prediction, dict) and prediction.get("id"):
            category_id = prediction["id"]
            print(f"  [listings] Predicted: {category_id}")
        else:
            raise ValueError(
                f"Could not predict category for title: {title}. "
                f"Response: {prediction}"
            )

    # Build pictures list — handle both URLs (source) and uploaded IDs
    pictures = []
    for img in images:
        if img.startswith("http"):
            pictures.append({"source": img})
        else:
            # Assume it's an already-uploaded picture ID
            pictures.append({"id": img})

    # Build attributes list from dict
    attr_list = [{"id": k, "value_name": v} for k, v in attributes.items()]

    # Free shipping threshold for MeLi Mexico
    free_shipping = price >= 299

    item_body = {
        "title": title,
        "category_id": category_id,
        "price": price,
        "currency_id": "MXN",
        "available_quantity": quantity,
        "buying_mode": "buy_it_now",
        "listing_type_id": listing_type,
        "condition": condition,
        "pictures": pictures,
        "attributes": attr_list,
        "shipping": {
            "mode": "me2",
            "free_shipping": free_shipping,
        },
    }

    # Only include description in the body if provided
    # (MeLi prefers POST /items/{id}/description separately, but some flows
    #  include it inline)
    if description:
        item_body["description"] = {"plain_text": description}

    print(f"  [listings] Prepared listing: {title}")
    print(f"             Category: {category_id} | Price: ${price:,.2f} MXN")
    print(f"             Images: {len(pictures)} | Attributes: {len(attr_list)}")
    print(f"             Free shipping: {free_shipping}")

    return item_body


# ------------------------------------------------------------------
# Image Upload
# ------------------------------------------------------------------

def upload_images(client: MeliClient, image_paths: list[str | Path]) -> list[str]:
    """
    Upload multiple local images to MeLi.
    Returns list of picture IDs (e.g. '984371-MLM12345_1').
    """
    picture_ids = []
    total = len(image_paths)

    for i, path in enumerate(image_paths, 1):
        path = Path(path)
        print(f"  [listings] Uploading image {i}/{total}: {path.name}")
        try:
            result = client.upload_image(path)
            pic_id = result.get("id", "")
            if pic_id:
                picture_ids.append(pic_id)
                print(f"             -> {pic_id}")
            else:
                print(f"             -> WARNING: no ID returned: {result}")
        except Exception as e:
            print(f"             -> ERROR: {e}")

    print(f"  [listings] Uploaded {len(picture_ids)}/{total} images successfully")
    return picture_ids


# ------------------------------------------------------------------
# Create Listing
# ------------------------------------------------------------------

def create_listing(
    client: MeliClient,
    item_data: dict,
    description: str | None = None,
    dry_run: bool = False,
) -> dict:
    """
    Create a MeLi listing.

    If dry_run=True, validates the item data without creating it.
    If description is provided, adds it after creation via POST /items/{id}/description.
    Returns the created item data (or validation result if dry_run).
    """
    if dry_run:
        print("  [listings] DRY RUN — validating item data...")
        # Remove description from body for validation (added separately)
        validate_data = {k: v for k, v in item_data.items() if k != "description"}
        result = client.validate_item(validate_data)
        print("  [listings] Validation result:")
        if isinstance(result, dict) and result.get("error"):
            print(f"             FAILED: {result.get('message', result)}")
        else:
            print("             PASSED — item data is valid")
        return result

    # Real creation
    print(f"  [listings] Creating listing: {item_data.get('title', '?')}")

    # Remove inline description — we'll add it separately
    create_data = {k: v for k, v in item_data.items() if k != "description"}
    result = client.create_item(create_data)

    item_id = result.get("id", "")
    permalink = result.get("permalink", "")
    print(f"  [listings] Created: {item_id}")
    if permalink:
        print(f"             Link: {permalink}")

    # Add description if provided (either from param or from item_data)
    desc_text = description or ""
    if not desc_text and isinstance(item_data.get("description"), dict):
        desc_text = item_data["description"].get("plain_text", "")

    if desc_text and item_id:
        print(f"  [listings] Adding description ({len(desc_text)} chars)...")
        try:
            client.add_description(item_id, desc_text)
            print("             Description added.")
        except Exception as e:
            print(f"             WARNING: Failed to add description: {e}")

    return result


# ------------------------------------------------------------------
# Update Operations
# ------------------------------------------------------------------

def update_price(client: MeliClient, item_id: str, new_price: float) -> dict:
    """Update just the price of an existing item."""
    print(f"  [listings] Updating price for {item_id}: ${new_price:,.2f} MXN")
    result = client.update_item(item_id, {"price": new_price})
    print(f"             Done.")
    return result


def update_stock(client: MeliClient, item_id: str, quantity: int) -> dict:
    """Update just the stock quantity of an existing item."""
    print(f"  [listings] Updating stock for {item_id}: {quantity} units")
    result = client.update_item(item_id, {"available_quantity": quantity})
    print(f"             Done.")
    return result


# ------------------------------------------------------------------
# Status Changes
# ------------------------------------------------------------------

def pause_listing(client: MeliClient, item_id: str) -> dict:
    """Pause a listing (set status to 'paused')."""
    print(f"  [listings] Pausing {item_id}")
    result = client.update_item(item_id, {"status": "paused"})
    print(f"             Status: paused")
    return result


def activate_listing(client: MeliClient, item_id: str) -> dict:
    """Activate a listing (set status to 'active')."""
    print(f"  [listings] Activating {item_id}")
    result = client.update_item(item_id, {"status": "active"})
    print(f"             Status: active")
    return result


def close_listing(client: MeliClient, item_id: str) -> dict:
    """Close a listing permanently (set status to 'closed')."""
    print(f"  [listings] Closing {item_id}")
    result = client.update_item(item_id, {"status": "closed"})
    print(f"             Status: closed")
    return result


# ------------------------------------------------------------------
# Listing Details
# ------------------------------------------------------------------

def get_listing_details(client: MeliClient, item_id: str) -> dict:
    """
    Fetch full item details and print a readable summary.
    Returns the raw item dict.
    """
    print(f"  [listings] Fetching details for {item_id}...\n")
    item = client.get_item(item_id)

    title = item.get("title", "?")
    price = item.get("price", 0)
    currency = item.get("currency_id", "MXN")
    status = item.get("status", "?")
    qty = item.get("available_quantity", 0)
    sold = item.get("sold_quantity", 0)
    category = item.get("category_id", "?")
    listing_type = item.get("listing_type_id", "?")
    condition = item.get("condition", "?")
    permalink = item.get("permalink", "")
    pictures = item.get("pictures", [])
    attributes = item.get("attributes", [])
    date_created = item.get("date_created", "?")
    shipping = item.get("shipping", {})

    print("  " + "=" * 60)
    print(f"  {title}")
    print("  " + "=" * 60)
    print(f"  ID:           {item_id}")
    print(f"  Price:        ${price:,.2f} {currency}")
    print(f"  Status:       {status}")
    print(f"  Condition:    {condition}")
    print(f"  Stock:        {qty} available / {sold} sold")
    print(f"  Category:     {category}")
    print(f"  Listing type: {listing_type}")
    print(f"  Created:      {date_created}")
    print(f"  Pictures:     {len(pictures)}")

    if shipping:
        mode = shipping.get("mode", "?")
        free = shipping.get("free_shipping", False)
        print(f"  Shipping:     {mode} {'(free)' if free else '(paid)'}")

    if attributes:
        print(f"\n  Attributes ({len(attributes)}):")
        for attr in attributes:
            name = attr.get("name", attr.get("id", "?"))
            val = attr.get("value_name", "—")
            print(f"    {name}: {val}")

    if permalink:
        print(f"\n  Link: {permalink}")

    print()
    return item


# ------------------------------------------------------------------
# Category Attributes
# ------------------------------------------------------------------

def get_required_attributes(client: MeliClient, category_id: str) -> list[dict]:
    """
    Get required attributes for a category.
    Returns list of {id, name, values} for attributes tagged as required.
    """
    print(f"  [listings] Fetching attributes for category {category_id}...")
    all_attrs = client.get_category_attributes(category_id)

    required = []
    for attr in all_attrs:
        tags = attr.get("tags", {})
        # MeLi marks required attributes with tags.required or tags.catalog_required
        is_required = (
            tags.get("required", False)
            or tags.get("catalog_required", False)
        )
        if is_required:
            values = []
            for v in attr.get("values", []):
                values.append({
                    "id": v.get("id", ""),
                    "name": v.get("name", ""),
                })
            required.append({
                "id": attr.get("id", ""),
                "name": attr.get("name", ""),
                "type": attr.get("value_type", ""),
                "values": values,
            })

    print(f"  [listings] Found {len(required)} required attributes (of {len(all_attrs)} total)\n")
    for attr in required:
        val_count = len(attr["values"])
        val_hint = f" ({val_count} allowed values)" if val_count else " (free text)"
        print(f"    [{attr['id']}] {attr['name']}{val_hint}")

    print()
    return required


# ------------------------------------------------------------------
# CLI
# ------------------------------------------------------------------

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("\n  Usage: python -m meli.listings <ITEM_ID>")
        print("  Example: python -m meli.listings MLM1234567890\n")
        sys.exit(1)

    item_id = sys.argv[1]
    client = MeliClient()
    get_listing_details(client, item_id)
