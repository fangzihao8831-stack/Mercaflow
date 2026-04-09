# -*- coding: utf-8 -*-
"""
MercaFlow — Orchestrator
Ties together the full listing creation pipeline.

Usage:
    from meli.orchestrator import create_listing
    
    result = create_listing(
        images=['photo1.jpg', 'photo2.jpg'],
        import_cost=90,
        brand='DAJIBA',
        dry_run=True,  # validate only, don't publish
    )
"""
import sys
import io
import time
from typing import Optional

try:
    sys.stdout.reconfigure(encoding='utf-8')
except (AttributeError, ValueError):
    pass

from meli.client import MeliClient
from meli.analyze import analyze_product, pick_best_category
from meli.auth import ensure_fresh_token
from meli.costs import calculate_costs, calculate_sell_price, make_attractive_price


# ===== CONSTANTS =====

# Mexico-only constants
SITE_ID = 'MLM'
CURRENCY = 'MXN'

DEFAULTS = {
    'brand': 'DAJIBA',
    'listing_type': 'gold_special',  # Clásica
    'quantity': 1,
    'target_margin_pct': 100,
    'condition': 'new',
    'warranty_type': 'Garantía del vendedor',
    'warranty_time': '30 días',
    'free_shipping': False,  # off by default, MeLi auto-enables when price >= $299
    'zip_code': '06600',  # CDMX default
    'placeholder_price': 9999.0,  # when no import cost
    'min_margin_pct': 20,  # warn if below this
    'free_shipping_threshold': 299,  # MXN, MeLi forces free shipping above this
}

# Attributes that are always the same
FIXED_ATTRS = {
    'ITEM_CONDITION': 'Nuevo',
    'SALE_FORMAT': 'Unidad',
    'UNITS_PER_PACK': '1',
    'SHIPMENT_PACKING': 'Caja',
    'IS_SUITABLE_FOR_SHIPMENT': 'Sí',
    'IS_KIT': 'No',
    'HAS_COMPATIBILITIES': 'No',
    'WITH_POSITIVE_IMPACT': 'No',
}


# ===== HELPER FUNCTIONS =====

def generate_fake_gtin():
    """Generate a valid EAN-13 barcode with correct check digit."""
    import random
    code = '789' + ''.join(str(random.randint(0, 9)) for _ in range(9))
    total = sum(int(d) * (1 if i % 2 == 0 else 3) for i, d in enumerate(code))
    check = (10 - (total % 10)) % 10
    return code + str(check)


def generate_sku(brand: str, category_id: str) -> str:
    """Generate a unique SKU."""
    ts = int(time.time())
    return f"{brand}-{category_id}-{ts}"


def classify_progress(step: str, status: str, message: str = ""):
    """Log step progress."""
    icon = {"start": "→", "ok": "✓", "warn": "⚠", "error": "✗", "info": "ℹ"}.get(status, "·")
    print(f"  [{step}] {icon} {message}")


# ===== MAIN ORCHESTRATOR =====

def create_listing(
    images: list,
    import_cost: Optional[float] = None,
    *,
    # Pricing
    brand: Optional[str] = None,
    listing_type: Optional[str] = None,
    target_margin_pct: Optional[float] = None,
    manual_price: Optional[float] = None,
    min_margin_pct: Optional[float] = None,
    # Product info
    quantity: Optional[int] = None,
    category_id: Optional[str] = None,
    notes: Optional[str] = None,
    gtin: Optional[str] = None,
    seller_sku: Optional[str] = None,
    # Package
    package_height_cm: Optional[float] = None,
    package_width_cm: Optional[float] = None,
    package_length_cm: Optional[float] = None,
    package_weight_g: Optional[float] = None,
    # Content overrides
    title_override: Optional[str] = None,
    description_override: Optional[str] = None,
    extra_attributes: Optional[dict] = None,
    # Warranty
    warranty_type: Optional[str] = None,
    warranty_time: Optional[str] = None,
    # Shipping
    free_shipping: Optional[bool] = None,
    zip_code: Optional[str] = None,
    # Publishing behavior
    dry_run: bool = True,
    auto_pause: bool = False,
) -> dict:
    """
    Full pipeline to create a MercadoLibre listing from product images.
    
    Args:
        images: list of image file paths (required)
        import_cost: your cost to acquire the product (optional)
        brand: override default brand
        listing_type: 'gold_special' (Clásica) or 'gold_pro' (Premium)
        target_margin_pct: desired profit % over import cost
        manual_price: force a specific price (skips auto-pricing)
        quantity: stock quantity
        category_id: force a specific category (skips auto-detection)
        notes: extra context for Claude
        package_*: package dimensions (guess if missing)
        gtin: real barcode if available
        seller_sku: custom SKU
        extra_attributes: dict to override specific attribute values
        dry_run: if True, validate only (don't publish)
        auto_pause: if True, create as paused instead of active
        zip_code: for shipping cost calculation
    
    Returns:
        dict with the full listing result
    """
    # Apply defaults
    brand = brand or DEFAULTS['brand']
    listing_type = listing_type or DEFAULTS['listing_type']
    target_margin_pct = target_margin_pct if target_margin_pct is not None else DEFAULTS['target_margin_pct']
    min_margin_pct = min_margin_pct if min_margin_pct is not None else DEFAULTS['min_margin_pct']
    quantity = quantity or DEFAULTS['quantity']
    zip_code = zip_code or DEFAULTS['zip_code']
    warranty_type = warranty_type or DEFAULTS['warranty_type']
    warranty_time = warranty_time or DEFAULTS['warranty_time']
    free_shipping = free_shipping if free_shipping is not None else DEFAULTS['free_shipping']
    extra_attributes = extra_attributes or {}
    
    # ===== STEP 0: Validate inputs =====
    print("\n" + "=" * 60)
    print("MERCAFLOW ORCHESTRATOR")
    print("=" * 60 + "\n")
    
    warnings = []
    
    if not images or len(images) == 0:
        return {"status": "error", "message": "At least one image is required"}
    
    classify_progress("INPUT", "ok", f"{len(images)} image(s)")
    
    if import_cost is None:
        warnings.append("No import cost — listing will be paused at placeholder price")
        classify_progress("INPUT", "warn", "No import cost → placeholder price mode")
        auto_pause = True
    else:
        classify_progress("INPUT", "ok", f"Import cost: ${import_cost}")
    
    if not package_weight_g:
        warnings.append("No package weight — will estimate (may affect shipping cost)")
        classify_progress("INPUT", "warn", "No package dimensions")

    # Proactive token refresh — make sure the access token has at least 1h life left
    # so the publish flow (steps 8–13) doesn't crash mid-run.
    if not dry_run:
        try:
            ensure_fresh_token(min_remaining_seconds=3600)
            classify_progress("AUTH", "ok", "Token fresh (≥1h remaining)")
        except RuntimeError as e:
            return {"status": "error", "step": 0, "message": str(e)}

    # ===== STEP 1: Quick Claude analysis =====
    print()
    classify_progress("STEP 1", "start", "Quick product identification")
    t0 = time.time()
    
    try:
        quick = analyze_product(images, category_attributes=None, defaults={}, notes=notes)
        product_name = quick.get('product_name', '')
        classify_progress("STEP 1", "ok", f"Product: {product_name} ({time.time()-t0:.1f}s)")
    except Exception as e:
        return {"status": "error", "step": 1, "message": f"Quick analysis failed: {e}"}
    
    # ===== STEP 2: Find category =====
    classify_progress("STEP 2", "start", "Finding category")
    client = MeliClient()

    try:
        if category_id:
            classify_progress("STEP 2", "info", f"Using forced category: {category_id}")
        else:
            results = client.get(f'/sites/{SITE_ID}/domain_discovery/search',
                                params={'q': product_name})
            if not isinstance(results, list) or not results:
                return {"status": "error", "step": 2, "message": "No category found"}

            if len(results) == 1:
                category_id = results[0]['category_id']
                cat_name = results[0].get('category_name', '?')
                classify_progress("STEP 2", "ok", f"{category_id}: {cat_name} (only candidate)")
            else:
                # Multiple candidates — let Claude pick the best fit from the top 5
                top_candidates = results[:5]
                try:
                    category_id = pick_best_category(images, product_name, top_candidates)
                    cat_name = next(
                        (c.get('category_name', '?') for c in top_candidates if c.get('category_id') == category_id),
                        '?',
                    )
                    classify_progress("STEP 2", "ok", f"{category_id}: {cat_name} (LLM picked from {len(top_candidates)})")
                except Exception as e:
                    # Fallback to first result if Claude pick fails
                    category_id = results[0]['category_id']
                    cat_name = results[0].get('category_name', '?')
                    classify_progress("STEP 2", "warn", f"LLM pick failed ({e}), using first: {category_id}: {cat_name}")
    except Exception as e:
        return {"status": "error", "step": 2, "message": f"Category search failed: {e}"}
    
    # ===== STEP 3: Get category attributes =====
    classify_progress("STEP 3", "start", "Fetching category attributes")
    try:
        category_attrs = client.get_category_attributes(category_id)
        classify_progress("STEP 3", "ok", f"{len(category_attrs)} attributes")
    except Exception as e:
        return {"status": "error", "step": 3, "message": f"Failed to get attributes: {e}"}
    
    # Get category settings (for max title length, etc.)
    try:
        cat_info = client.get_category(category_id)
        max_title = cat_info.get('settings', {}).get('max_title_length', 60)
    except:
        max_title = 60
    
    # ===== STEP 4: Full Claude analysis with attributes =====
    print()
    classify_progress("STEP 4", "start", "Full content generation")
    t4 = time.time()

    # Build defaults for Claude
    claude_defaults = {
        'BRAND': brand,
        **FIXED_ATTRS,
    }
    if seller_sku:
        claude_defaults['SELLER_SKU'] = seller_sku
    if gtin:
        claude_defaults['GTIN'] = gtin

    if title_override and description_override:
        # Both content fields are user-supplied — skip the expensive Claude call.
        # Attributes will come from `extra_attributes` + claude_defaults only.
        # Required category fields not in extra_attributes will be caught by validate_item (STEP 9).
        classify_progress("STEP 4", "info", "Skipped (title + description both overridden)")
        warnings.append("Claude content generation skipped — required category attributes must be passed via extra_attributes")
        analysis = {
            'product_name': product_name,
            'family_name': title_override,
            'description': description_override,
            'title_alternatives': [],
            'attributes': dict(claude_defaults),
            'search_keywords': [],
        }
    else:
        try:
            analysis = analyze_product(images, category_attributes=category_attrs, defaults=claude_defaults, notes=notes)
            classify_progress("STEP 4", "ok", f"Generated content ({time.time()-t4:.1f}s)")
        except Exception as e:
            return {"status": "error", "step": 4, "message": f"Full analysis failed: {e}"}
    
    # ===== STEP 5: Apply defaults and logic =====
    print()
    classify_progress("STEP 5", "start", "Applying defaults")
    
    attributes = analysis.get('attributes', {})
    family_name = analysis.get('family_name', product_name)
    description = analysis.get('description', '')
    
    # Trim title to max length
    if len(family_name) > max_title:
        family_name = family_name[:max_title].rstrip()
        classify_progress("STEP 5", "warn", f"Title trimmed to {max_title} chars")
    
    # Auto-generate SKU if missing
    if 'SELLER_SKU' not in attributes:
        attributes['SELLER_SKU'] = generate_sku(brand, category_id)
    
    # Auto-generate fake GTIN if missing
    if 'GTIN' not in attributes:
        attributes['GTIN'] = generate_fake_gtin()
        warnings.append("GTIN was auto-generated (fake)")
    
    # Package dimensions
    pkg_height = package_height_cm or 10
    pkg_width = package_width_cm or 20
    pkg_length = package_length_cm or 20
    pkg_weight = package_weight_g or 500
    
    attributes['SELLER_PACKAGE_HEIGHT'] = f"{pkg_height} cm"
    attributes['SELLER_PACKAGE_WIDTH'] = f"{pkg_width} cm"
    attributes['SELLER_PACKAGE_LENGTH'] = f"{pkg_length} cm"
    attributes['SELLER_PACKAGE_WEIGHT'] = f"{pkg_weight} g"
    
    # Apply extra_attributes overrides
    for k, v in extra_attributes.items():
        attributes[k] = v
    
    classify_progress("STEP 5", "ok", f"{len(attributes)} attributes ready")
    
    # ===== STEP 6: Calculate price =====
    classify_progress("STEP 6", "start", "Calculating price")
    
    if manual_price:
        price = manual_price
        classify_progress("STEP 6", "info", f"Manual price: ${price}")
    elif import_cost is None:
        price = DEFAULTS['placeholder_price']
        classify_progress("STEP 6", "warn", f"Placeholder price: ${price} (no import cost)")
    else:
        # Get real commission from API
        lp_data = client.get_listing_prices(
            price=import_cost * 3,  # start with 3x guess
            category_id=category_id,
            listing_type_id=listing_type
        )
        commission_pct = 15  # default
        if isinstance(lp_data, list):
            for lp in lp_data:
                if lp.get('listing_type_id') == listing_type:
                    commission_pct = lp.get('sale_fee_details', {}).get('percentage_fee', 15)
                    break
        elif isinstance(lp_data, dict):
            commission_pct = lp_data.get('sale_fee_details', {}).get('percentage_fee', 15)
        
        # Calculate and round to attractive
        raw = calculate_sell_price(import_cost, target_margin_pct, commission_pct, pkg_weight / 1000)
        price = make_attractive_price(raw)
        classify_progress("STEP 6", "ok", f"${price} (commission {commission_pct}%)")
    
    # ===== STEP 7: Build listing body =====
    classify_progress("STEP 7", "start", "Building listing")
    
    # Format attributes for MeLi API
    attr_list = [{'id': k, 'value_name': str(v)} for k, v in attributes.items()]
    
    # Apply title/description overrides
    if title_override:
        family_name = title_override[:max_title]
    if description_override:
        description = description_override
    
    # Auto-enable free shipping if price >= threshold (MeLi forces it)
    effective_free_shipping = free_shipping or (price >= DEFAULTS['free_shipping_threshold'])
    
    listing_body = {
        'family_name': family_name,
        'category_id': category_id,
        'price': price,
        'currency_id': CURRENCY,
        'available_quantity': quantity,
        'buying_mode': 'buy_it_now',
        'listing_type_id': listing_type,
        'condition': 'new',
        'pictures': [],  # will fill after upload
        'attributes': attr_list,
        'shipping': {
            'mode': 'me2',
            'free_shipping': effective_free_shipping,
        },
        'sale_terms': [
            {'id': 'WARRANTY_TYPE', 'value_name': warranty_type},
            {'id': 'WARRANTY_TIME', 'value_name': warranty_time},
        ],
    }
    
    ship_label = "free shipping" if effective_free_shipping else "buyer pays shipping"
    classify_progress("STEP 7", "ok", f"Price ${price}, {quantity} units, {listing_type}, {ship_label}")
    
    # ===== DRY RUN: return preview without publishing =====
    if dry_run:
        print()
        classify_progress("DRY RUN", "info", "Stopping here (dry_run=True)")
        return {
            "status": "dry_run",
            "preview": {
                "family_name": family_name,
                "title_alternatives": analysis.get('title_alternatives', []),
                "price": price,
                "description": description,
                "attributes": attributes,
                "category_id": category_id,
                "listing_type": listing_type,
                "quantity": quantity,
                "images": images,
            },
            "warnings": warnings,
            "import_cost": import_cost,
        }
    
    # ===== STEP 8: Upload images =====
    print()
    classify_progress("STEP 8", "start", f"Uploading {len(images)} images")
    
    picture_ids = []
    for i, img_path in enumerate(images):
        try:
            result = client.upload_image(img_path)
            picture_ids.append(result.get('id'))
            classify_progress("STEP 8", "ok", f"Image {i+1}/{len(images)}")
        except Exception as e:
            return {"status": "error", "step": 8, "message": f"Image {i+1} upload failed: {e}"}
    
    listing_body['pictures'] = [{'id': pid} for pid in picture_ids]
    
    # ===== STEP 9: Validate =====
    classify_progress("STEP 9", "start", "Validating listing")
    try:
        client.validate_item(listing_body)
        classify_progress("STEP 9", "ok", "Validation passed")
    except Exception as e:
        return {"status": "error", "step": 9, "message": f"Validation failed: {e}", "listing_body": listing_body}
    
    # ===== STEP 10: Create listing =====
    classify_progress("STEP 10", "start", "Creating listing on MeLi")
    try:
        item = client.create_item(listing_body)
        item_id = item.get('id')
        permalink = item.get('permalink', '')
        classify_progress("STEP 10", "ok", f"{item_id}")
    except Exception as e:
        return {"status": "error", "step": 10, "message": f"Create failed: {e}"}
    
    # ===== STEP 11: Add description =====
    classify_progress("STEP 11", "start", "Adding description")
    try:
        client.add_description(item_id, description)
        classify_progress("STEP 11", "ok", "Description added")
    except Exception as e:
        classify_progress("STEP 11", "warn", f"Description failed: {e}")
    
    # ===== STEP 12: Verify profit =====
    print()
    classify_progress("STEP 12", "start", "Verifying profit via API")
    profit_verified = False
    margin_guard_triggered = False
    commission = shipping = taxes = you_receive = profit = margin = None

    try:
        # Commission
        lp = client.get_listing_prices(price=price, category_id=category_id, listing_type_id=listing_type)
        commission = 0
        if isinstance(lp, list):
            for l in lp:
                if l.get('listing_type_id') == listing_type:
                    commission = l.get('sale_fee_amount', 0)
                    break
        elif isinstance(lp, dict):
            commission = lp.get('sale_fee_amount', 0)

        # Shipping
        ship_data = client.get_shipping_options(item_id, zip_code)
        shipping = 0
        if ship_data.get('options'):
            shipping = ship_data['options'][0].get('list_cost', 0)

        # Taxes (Mexico effective rate ~9.05% of listed price; see docs/meli-mexico-complete-cost-breakdown.md)
        tax_base = price / 1.16
        taxes = tax_base * 0.105

        you_receive = price - commission - shipping - taxes
        profit = (you_receive - import_cost) if import_cost else None
        margin = (profit / import_cost * 100) if import_cost and import_cost > 0 else None

        profit_verified = True  # Only true once all the math above succeeded

        classify_progress("STEP 12", "ok", f"Commission ${commission:.2f}, Shipping ${shipping:.2f}, Taxes ${taxes:.2f}")
        classify_progress("STEP 12", "ok", f"You receive: ${you_receive:.2f}")
        if profit is not None:
            classify_progress("STEP 12", "ok", f"Profit: ${profit:.2f} ({margin:.0f}% margin)")

    except Exception as e:
        # Treat verification failure as unsafe — force the margin guard to pause the listing
        classify_progress("STEP 12", "error", f"PROFIT NOT VERIFIED: {e}")
        warnings.append(f"PROFIT NOT VERIFIED ({e}) — listing auto-paused as safety")
        margin_guard_triggered = True

    # ===== STEP 13: Margin guard + auto-pause =====
    final_status = "active"

    # Margin guard — force pause if verified margin is below threshold
    # (margin_guard_triggered may already be True from a verification failure above)
    if profit_verified and margin is not None and margin < min_margin_pct:
        warnings.append(f"Low margin: {margin:.0f}% (below {min_margin_pct}% threshold) — listing auto-paused")
        classify_progress("GUARD", "warn", f"Margin {margin:.0f}% below {min_margin_pct}% — forcing pause")
        margin_guard_triggered = True

    # Auto-pause if requested OR if margin guard triggered
    if auto_pause or margin_guard_triggered:
        try:
            client.update_item(item_id, {'status': 'paused'})
            final_status = "paused"
            if margin_guard_triggered and not profit_verified:
                reason = "profit not verified"
            elif margin_guard_triggered:
                reason = "margin guard"
            else:
                reason = "auto_pause flag"
            classify_progress("STEP 13", "ok", f"Paused ({reason})")
        except Exception as e:
            classify_progress("STEP 13", "error", f"Failed to pause: {e}")
            warnings.append(f"Listing is ACTIVE but should be paused: {e}")
    
    # ===== DONE =====
    print()
    print("=" * 60)
    print(f"✓ LISTING CREATED: {item_id}")
    print(f"  URL: {permalink}")
    print(f"  Status: {final_status}")
    if profit_verified and profit is not None:
        print(f"  Profit: ${profit:.2f} ({margin:.0f}% margin)")
    elif not profit_verified:
        print(f"  ⚠ PROFIT NOT VERIFIED — listing was auto-paused for safety")
    print("=" * 60)

    return {
        "status": "created",
        "item_id": item_id,
        "permalink": permalink,
        "listing_status": final_status,
        "price": price,
        "family_name": family_name,
        "category_id": category_id,
        "costs": {
            "commission": commission,
            "shipping": shipping,
            "taxes": taxes,
            "you_receive": you_receive,
        },
        "profit": profit,
        "margin_pct": margin,
        "profit_verified": profit_verified,
        "warnings": warnings,
    }


if __name__ == "__main__":
    # Test with the jewelry box
    result = create_listing(
        images=['test-products/stationery/product-08.jpg'],
        import_cost=30,
        package_height_cm=6,
        package_width_cm=9,
        package_length_cm=9,
        package_weight_g=150,
        dry_run=True,  # don't actually publish
    )
    
    print("\n\n" + "=" * 60)
    print("RESULT:")
    print("=" * 60)
    import json
    print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
