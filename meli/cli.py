# -*- coding: utf-8 -*-
"""
MercaFlow — MercadoLibre CLI
Main entry point for all MeLi operations.

Usage:
    python meli/cli.py auth          — Test authentication
    python meli/cli.py items         — List all your items
    python meli/cli.py item <ID>     — Show item details
    python meli/cli.py costs <price> <commission%> [weight_kg]  — Cost breakdown
    python meli/cli.py price <import_cost> <target_margin%> <commission%> [weight_kg]  — Calculate sell price
    python meli/cli.py category <title>  — Predict category for a product title
    python meli/cli.py trends        — Show trending searches in Mexico
    python meli/cli.py create        — Interactive listing creator
    python meli/cli.py visits <ID>   — Show item visits
    python meli/cli.py performance <ID>  — Show item quality score
"""
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from meli.client import MeliClient, MeliAPIError
from meli.costs import calculate_costs, calculate_sell_price, make_attractive_price, print_cost_breakdown
from meli.listings import get_listing_details, get_required_attributes, prepare_listing, create_listing


def cmd_auth():
    """Test authentication and show user info."""
    client = MeliClient()
    user = client.get_user()
    print(f"\n  [OK] Authenticated!")
    print(f"  User ID:    {user['id']}")
    print(f"  Nickname:   {user['nickname']}")
    print(f"  Country:    {user.get('country_id', '?')}")
    print(f"  Permalink:  {user.get('permalink', '?')}")
    
    # Show listing capacity
    try:
        caps = client.get("/marketplace/users/cap")
        if isinstance(caps, list):
            for cap in caps:
                if cap.get("site_id") == "MLM":
                    print(f"\n  MLM Listings: {cap.get('total_items', 0)} / {cap.get('quota', '?')} quota")
    except:
        pass
    print()


def cmd_items():
    """List all seller items."""
    client = MeliClient()
    user = client.get_user()
    user_id = user["id"]
    
    data = client.search_items(user_id=user_id, limit=50)
    item_ids = data.get("results", [])
    total = data.get("paging", {}).get("total", 0)
    
    print(f"\n  {total} item(s) found\n")
    
    if not item_ids:
        return
    
    items = client.get_items(item_ids)
    
    active = [i for i in items if i.get("status") == "active"]
    paused = [i for i in items if i.get("status") == "paused"]
    closed = [i for i in items if i.get("status") == "closed"]
    
    for label, group in [("ACTIVE", active), ("PAUSED", paused), ("CLOSED", closed)]:
        if not group:
            continue
        print(f"  --- {label} ({len(group)}) ---\n")
        for item in group:
            sold = item.get("sold_quantity", 0)
            stock = item.get("available_quantity", 0)
            price = item.get("price", 0)
            print(f"    {item['id']}  ${price:,.2f}  stock:{stock} sold:{sold}")
            print(f"    {item.get('title', '?')}")
            print()


def cmd_item(item_id):
    """Show detailed item info."""
    client = MeliClient()
    get_listing_details(client, item_id)


def cmd_costs(price, commission_pct, weight_kg=0.5):
    """Show cost breakdown for a price point."""
    costs = calculate_costs(price, commission_pct, weight_kg)
    print()
    print_cost_breakdown(costs)
    
    # Also show attractive price suggestion
    attractive = make_attractive_price(price)
    if attractive != price:
        print(f"\n  Attractive price suggestion: ${attractive:,.2f}")
        costs2 = calculate_costs(attractive, commission_pct, weight_kg)
        print(f"  You'd receive: ${costs2['you_receive']:,.2f} (+${costs2['you_receive'] - costs['you_receive']:,.2f})")
    print()


def cmd_price(import_cost, target_margin, commission_pct, weight_kg=0.5):
    """Calculate sell price from import cost + target margin."""
    raw_price = calculate_sell_price(import_cost, target_margin, commission_pct, weight_kg)
    attractive = make_attractive_price(raw_price)
    
    print(f"\n  Import cost:    ${import_cost:,.2f}")
    print(f"  Target margin:  {target_margin}%")
    print(f"  Commission:     {commission_pct}%")
    print(f"  Weight:         {weight_kg}kg")
    print(f"\n  Raw price:      ${raw_price:,.2f}")
    print(f"  Attractive:     ${attractive:,.2f}")
    
    # Show breakdown at attractive price
    costs = calculate_costs(attractive, commission_pct, weight_kg)
    print()
    print_cost_breakdown(costs)
    
    profit = costs["you_receive"] - import_cost
    actual_margin = (profit / import_cost) * 100 if import_cost > 0 else 0
    print(f"\n  Your profit:    ${profit:,.2f}")
    print(f"  Actual margin:  {actual_margin:.1f}%")
    print()


def cmd_category(title):
    """Predict category for a product title."""
    client = MeliClient()
    result = client.predict_category(title)
    
    if isinstance(result, list) and result:
        for pred in result[:3]:
            cat_id = pred.get("id", "?")
            cat_name = pred.get("name", "?")
            prob = pred.get("prediction_probability", "?")
            domain = pred.get("domain_id", "?")
            print(f"\n  Category: {cat_id}")
            print(f"  Name:     {cat_name}")
            print(f"  Domain:   {domain}")
            print(f"  Prob:     {prob}")
            
            # Show path
            path = pred.get("path_from_root", [])
            if path:
                path_str = " > ".join(p.get("category_name", "?") for p in path)
                print(f"  Path:     {path_str}")
            
            # Show required attributes
            print(f"\n  Required attributes for {cat_id}:")
            attrs = get_required_attributes(client, cat_id)
            for attr in attrs[:10]:
                values = attr.get("values", [])
                val_str = ", ".join(v.get("name", "?") for v in values[:5])
                if len(values) > 5:
                    val_str += f"... (+{len(values)-5} more)"
                tag = " [REQUIRED]" if attr.get("required") else " [catalog]"
                print(f"    {attr['id']}: {attr['name']}{tag}")
                if val_str:
                    print(f"      Values: {val_str}")
    else:
        print(f"\n  No category prediction for: {title}")
    print()


def cmd_trends():
    """Show trending searches in Mexico."""
    client = MeliClient()
    trends = client.get_trends()
    
    if isinstance(trends, list):
        print(f"\n  Top {len(trends)} trending searches in MLM:\n")
        for i, trend in enumerate(trends[:20], 1):
            keyword = trend.get("keyword", "?")
            url = trend.get("url", "")
            print(f"  {i:2d}. {keyword}")
    else:
        print("  Could not fetch trends")
    print()


def cmd_visits(item_id):
    """Show item visits."""
    client = MeliClient()
    try:
        data = client.get_item_visits(item_id)
        print(f"\n  Visits for {item_id}:")
        if isinstance(data, dict):
            for key, val in data.items():
                print(f"    {key}: {val}")
        else:
            print(f"    {data}")
    except MeliAPIError as e:
        print(f"  Error: {e}")
    print()


def cmd_performance(item_id):
    """Show item quality/performance score."""
    client = MeliClient()
    try:
        data = client.get_item_performance(item_id)
        print(f"\n  Performance for {item_id}:")
        if isinstance(data, dict):
            print(f"    Score: {data.get('score', '?')}")
            print(f"    Level: {data.get('level', '?')} ({data.get('level_wording', '?')})")
            buckets = data.get("buckets", [])
            for bucket in buckets:
                name = bucket.get("name", "?")
                print(f"\n    [{name}]")
                for rule in bucket.get("rules", []):
                    status = rule.get("status", "?")
                    label = rule.get("label", rule.get("id", "?"))
                    icon = "[OK]" if status == "done" else "[!!]" if status == "warning" else "[--]"
                    print(f"      {icon} {label}: {status}")
        else:
            print(f"    {data}")
    except MeliAPIError as e:
        print(f"  Error: {e}")
    print()


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return
    
    cmd = sys.argv[1].lower()
    
    try:
        if cmd == "auth":
            cmd_auth()
        
        elif cmd == "items":
            cmd_items()
        
        elif cmd == "item" and len(sys.argv) >= 3:
            cmd_item(sys.argv[2])
        
        elif cmd == "costs" and len(sys.argv) >= 4:
            price = float(sys.argv[2])
            commission = float(sys.argv[3])
            weight = float(sys.argv[4]) if len(sys.argv) >= 5 else 0.5
            cmd_costs(price, commission, weight)
        
        elif cmd == "price" and len(sys.argv) >= 5:
            import_cost = float(sys.argv[2])
            margin = float(sys.argv[3])
            commission = float(sys.argv[4])
            weight = float(sys.argv[5]) if len(sys.argv) >= 6 else 0.5
            cmd_price(import_cost, margin, commission, weight)
        
        elif cmd == "category" and len(sys.argv) >= 3:
            title = " ".join(sys.argv[2:])
            cmd_category(title)
        
        elif cmd == "trends":
            cmd_trends()
        
        elif cmd == "visits" and len(sys.argv) >= 3:
            cmd_visits(sys.argv[2])
        
        elif cmd == "performance" and len(sys.argv) >= 3:
            cmd_performance(sys.argv[2])
        
        else:
            print(__doc__)
    
    except MeliAPIError as e:
        print(f"\n  API Error: {e}\n")
    except KeyboardInterrupt:
        print("\n  Cancelled.\n")


if __name__ == "__main__":
    main()
