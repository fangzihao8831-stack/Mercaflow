"""
MercaFlow — MercadoLibre Mexico cost calculator.

Calculates the full cost breakdown (commission, fixed fee, shipping, ISR/IVA
retention) for a product listed on MLM so you know exactly what you receive
BEFORE publishing the listing.

Tax rules: Mexico 2026
  - Product IVA is 16 % included in the listed price.
  - ISR retention  = (price / 1.16) * 2.5 %
  - IVA retention  = (price / 1.16) * 8 %   (50 % of 16 %)
"""

from __future__ import annotations

import math
import sys
from typing import Dict

# ---------------------------------------------------------------------------
# Lookup tables
# ---------------------------------------------------------------------------

# (max_weight_g, base_shipping_cost_MXN)
_SHIPPING_TABLE: list[tuple[int, float]] = [
    (300,   131.0),
    (500,   140.0),
    (1000,  149.0),
    (2000,  169.0),
    (3000,  190.0),
    (4000,  206.0),
    (5000,  220.0),
    (7000,  245.0),
    (9000,  279.0),
    (12000, 323.0),
    (15000, 380.0),
    (20000, 445.0),
    (30000, 563.0),
]

# (max_price_exclusive, fixed_fee)  — last entry uses math.inf
_FIXED_FEE_TABLE: list[tuple[float, float]] = [
    (99.0,   25.0),
    (149.0,  30.0),
    (299.0,  37.0),
    (math.inf, 0.0),
]


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _lookup_fixed_fee(price: float) -> float:
    """Return the per-unit fixed fee for *price* MXN."""
    for threshold, fee in _FIXED_FEE_TABLE:
        if price < threshold:
            return fee
    return 0.0


def _lookup_shipping_base(weight_kg: float) -> float:
    """Return base shipping cost for *weight_kg*."""
    weight_g = weight_kg * 1000.0
    for max_g, cost in _SHIPPING_TABLE:
        if weight_g <= max_g:
            return cost
    # Heavier than 30 kg — use the last tier
    return _SHIPPING_TABLE[-1][1]


def _shipping_discount_pct(price: float) -> int:
    """Return the shipping-discount percentage based on sale price."""
    if price >= 499.0:
        return 50
    if price >= 299.0:
        return 60
    return 30  # new products < $299


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def calculate_costs(
    price: float,
    category_commission_pct: float,
    weight_kg: float = 0.5,
    listing_type: str = "gold_special",
) -> Dict[str, float]:
    """Return a full cost-breakdown dict for a product listed at *price* MXN.

    Parameters
    ----------
    price : float
        Listed sale price (IVA-included).
    category_commission_pct : float
        Category commission as a percentage (e.g. 15.0 for 15 %).
    weight_kg : float
        Packed weight in kilograms.  Defaults to 0.5 kg.
    listing_type : str
        MeLi listing type.  Currently only ``"gold_special"`` (Premium) is
        modelled; kept for future expansion.
    """
    # Commission
    commission = round(price * category_commission_pct / 100.0, 2)

    # Fixed fee
    fixed_fee = _lookup_fixed_fee(price)

    # Shipping
    shipping_base = _lookup_shipping_base(weight_kg)
    discount_pct = _shipping_discount_pct(price)
    shipping_cost = round(shipping_base * (1.0 - discount_pct / 100.0), 2)

    # Taxes
    tax_base = round(price / 1.16, 2)
    isr_retention = round(tax_base * 0.025, 2)
    iva_retention = round(tax_base * 0.08, 2)
    total_taxes = round(isr_retention + iva_retention, 2)

    # Totals
    total_deductions = round(commission + fixed_fee + shipping_cost + total_taxes, 2)
    you_receive = round(price - total_deductions, 2)
    margin_pct = round(you_receive / price * 100.0, 2) if price else 0.0

    return {
        "sale_price": price,
        "commission_pct": category_commission_pct,
        "commission": commission,
        "fixed_fee": fixed_fee,
        "shipping_base": shipping_base,
        "shipping_discount_pct": discount_pct,
        "shipping_cost": shipping_cost,
        "tax_base": tax_base,
        "isr_retention": isr_retention,
        "iva_retention": iva_retention,
        "total_taxes": total_taxes,
        "total_deductions": total_deductions,
        "you_receive": you_receive,
        "margin_pct": margin_pct,
    }


def calculate_sell_price(
    import_cost: float,
    target_margin_pct: float,
    category_commission_pct: float,
    weight_kg: float = 0.5,
) -> float:
    """Reverse-calculate the listing price that yields *target_margin_pct* on
    your import cost.

    Margin definition::

        margin = (you_receive - import_cost) / import_cost * 100

    Uses binary search because the deduction schedule (fixed fees, shipping
    tiers, discount tiers) is non-linear.
    """
    # Lower bound: at minimum you must cover import_cost
    lo = import_cost
    # Upper bound: generous 10x markup should always be enough
    hi = import_cost * 10.0

    for _ in range(200):  # plenty of iterations for sub-centavo precision
        mid = (lo + hi) / 2.0
        costs = calculate_costs(mid, category_commission_pct, weight_kg)
        actual_margin = (costs["you_receive"] - import_cost) / import_cost * 100.0
        if actual_margin < target_margin_pct:
            lo = mid
        else:
            hi = mid
        if abs(hi - lo) < 0.01:
            break

    # Return the upper bound (ceil to the centavo) to guarantee >= target
    return round(math.ceil(hi * 100.0) / 100.0, 2)


def make_attractive_price(raw_price: float) -> float:
    """Round *raw_price* UP to the nearest psychologically attractive price.

    Rules
    -----
    - <  100  : nearest  .95  above  (e.g. 87.23  -> 89.95)
    - 100-499 : nearest 9.95  above  (e.g. 241.23 -> 249.95)
    - 500-999 : nearest 49.95 above  (e.g. 673.50 -> 699.95)
    - 1000-4999: nearest 99.95 above (e.g. 3241   -> 3299.95)
    - >= 5000 : nearest 499.95 above (e.g. 11150  -> 11499.95)
    """
    if raw_price < 100.0:
        step, tail = 10.0, 9.95
    elif raw_price < 500.0:
        step, tail = 10.0, 9.95
    elif raw_price < 1000.0:
        step, tail = 50.0, 49.95
    elif raw_price < 5000.0:
        step, tail = 100.0, 99.95
    else:
        step, tail = 500.0, 499.95

    # Compute the attractive price at or above raw_price.
    # Pattern: base * step + tail  where base is an integer.
    # e.g. step=10, tail=9.95 => 9.95, 19.95, 29.95, ...
    # We want the smallest base such that base*step + tail >= raw_price
    # but tail = step - 0.05, so base*step + step - 0.05 = (base+1)*step - 0.05
    # Rewrite: candidate = n * step - 0.05  for integer n >= 1
    # We need n * step - 0.05 >= raw_price  =>  n >= (raw_price + 0.05) / step
    n = math.ceil((raw_price + 0.05) / step)
    if n < 1:
        n = 1
    candidate = round(n * step - 0.05, 2)
    return candidate


def print_cost_breakdown(costs: Dict[str, float]) -> None:
    """Pretty-print a cost breakdown dict to stdout."""
    p = costs
    w = 22  # label width

    print("=" * 50)
    print(f"{'Precio de venta':<{w}} ${p['sale_price']:>10,.2f}")
    print("-" * 50)
    print(f"{'Comision (' + str(p['commission_pct']) + '%)':<{w}} -${p['commission']:>9,.2f}")
    print(f"{'Cargo fijo':<{w}} -${p['fixed_fee']:>9,.2f}")
    print(f"{'Envio base':<{w}}  ${p['shipping_base']:>9,.2f}")
    print(f"{'  Descuento envio':<{w}}  {p['shipping_discount_pct']:>9d}%")
    print(f"{'  Costo envio':<{w}} -${p['shipping_cost']:>9,.2f}")
    print(f"{'Base gravable':<{w}}  ${p['tax_base']:>9,.2f}")
    print(f"{'  ISR retencion (2.5%)':<{w}} -${p['isr_retention']:>9,.2f}")
    print(f"{'  IVA retencion (8%)':<{w}} -${p['iva_retention']:>9,.2f}")
    print(f"{'  Total impuestos':<{w}} -${p['total_taxes']:>9,.2f}")
    print("-" * 50)
    print(f"{'Total deducciones':<{w}} -${p['total_deductions']:>9,.2f}")
    print(f"{'TU RECIBES':<{w}} ${p['you_receive']:>10,.2f}")
    print(f"{'Margen sobre precio':<{w}} {p['margin_pct']:>10.2f}%")
    print("=" * 50)


# ---------------------------------------------------------------------------
# CLI demo
# ---------------------------------------------------------------------------

def _main() -> None:
    # Force UTF-8 on Windows consoles
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[union-attr]

    print("\n*** MercaFlow — Calculadora de costos MeLi Mexico ***\n")

    # --- Example 1: Oura Ring ---
    print("[1] Oura Ring — $11,150 MXN, 15% comision, 0.1 kg")
    c1 = calculate_costs(11150.0, 15.0, weight_kg=0.1)
    print_cost_breakdown(c1)

    # --- Example 2: Cheap product ---
    print("\n[2] Producto barato — $150 MXN, 14% comision, 0.5 kg")
    c2 = calculate_costs(150.0, 14.0, weight_kg=0.5)
    print_cost_breakdown(c2)

    # --- Example 3: Mid product ---
    print("\n[3] Producto medio — $450 MXN, 12% comision, 1 kg")
    c3 = calculate_costs(450.0, 12.0, weight_kg=1.0)
    print_cost_breakdown(c3)

    # --- Reverse calculation demo ---
    print("\n--- Calculo inverso ---")
    import_cost = 2500.0
    target_margin = 80.0
    raw = calculate_sell_price(import_cost, target_margin, 15.0, weight_kg=0.3)
    attractive = make_attractive_price(raw)
    print(f"Costo importacion: ${import_cost:,.2f}")
    print(f"Margen objetivo:   {target_margin:.0f}%")
    print(f"Precio calculado:  ${raw:,.2f}")
    print(f"Precio atractivo:  ${attractive:,.2f}")
    print()
    final = calculate_costs(attractive, 15.0, weight_kg=0.3)
    print_cost_breakdown(final)
    actual_margin = (final["you_receive"] - import_cost) / import_cost * 100.0
    print(f"Margen real sobre costo: {actual_margin:.2f}%")
    print()


if __name__ == "__main__":
    _main()
