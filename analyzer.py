"""
analyzer.py  –  Inventory Business Intelligence
Answers 5 key business questions from the INVENTORY dataset.

Author : Waqar Javed
Dataset: inventory.py  (200 products, 12 categories)
"""

import datetime
from collections import defaultdict
from inventory import INVENTORY

# ─── Shared helpers ───────────────────────────────────────────────────────────

TODAY = datetime.date.today()          # used for Q3 date arithmetic
LINE  = "─" * 72
DLINE = "═" * 72


def header(qnum: int, title: str) -> None:
    """Print a decorative question header."""
    print(f"\n{DLINE}")
    print(f"  Q{qnum}  │  {title}")
    print(DLINE)


def footer(summary: str) -> None:
    print(LINE)
    print(f"  {summary}")
    print(LINE)


# ══════════════════════════════════════════════════════════════════════════════
#  Q1 – Products below reorder point  (filter → sort → list comprehension)
# ══════════════════════════════════════════════════════════════════════════════

def q1_below_reorder() -> None:
    header(1, "TOP-10 PRODUCTS BELOW REORDER POINT")
    print("  These items need restocking before they run out of stock.\n")

    # 1. Filter  – keep only items where stock is below the threshold
    # 2. Sort    – most urgent first (largest shortfall = reorder_point - stock_qty)
    # 3. Slice   – take the worst 10
    below = [
        p for p in INVENTORY
        if p["stock_qty"] < p["reorder_point"]
    ]
    below.sort(key=lambda p: p["reorder_point"] - p["stock_qty"], reverse=True)
    top10 = below[:10]

    # Formatted table
    col = "{:<8} {:<32} {:<14} {:>9} {:>12} {:>10}"
    print(col.format("SKU", "Product Name", "Category",
                     "In Stock", "Reorder At", "Shortfall"))
    print("  " + "·" * 68)
    for p in top10:
        shortfall = p["reorder_point"] - p["stock_qty"]
        print("  " + col.format(
            p["sku"],
            p["name"][:31],
            p["category"][:13],
            p["stock_qty"],
            p["reorder_point"],
            f"–{shortfall}"
        ))

    footer(
        f"ACTION REQUIRED: {len(below)} products are below reorder point "
        f"({len(below)/len(INVENTORY)*100:.1f}% of catalogue). "
        f"Showing the 10 most urgent."
    )


# ══════════════════════════════════════════════════════════════════════════════
#  Q2 – Highest-margin product per category  (dict grouping + max)
# ══════════════════════════════════════════════════════════════════════════════

def q2_best_margin_per_category() -> None:
    header(2, "HIGHEST-MARGIN PRODUCT IN EACH CATEGORY")
    print("  Margin = (price − cost) / price × 100. "
          "These are your most profitable lines.\n")

    # Group products by category into a dict of lists
    by_cat: dict[str, list[dict]] = defaultdict(list)
    for p in INVENTORY:
        by_cat[p["category"]].append(p)

    # For each category, pick the product with the highest margin %
    winners = []
    for cat, products in sorted(by_cat.items()):
        best = max(
            products,
            key=lambda p: (p["price"] - p["cost"]) / p["price"]
        )
        margin = (best["price"] - best["cost"]) / best["price"] * 100
        winners.append((cat, best, margin))

    col = "{:<14} {:<32} {:>8} {:>8} {:>9}"
    print("  " + col.format("Category", "Product", "Price", "Cost", "Margin %"))
    print("  " + "·" * 68)
    for cat, p, margin in winners:
        print("  " + col.format(
            cat[:13],
            p["name"][:31],
            f"${p['price']:.2f}",
            f"${p['cost']:.2f}",
            f"{margin:.1f}%"
        ))

    avg_margin = sum(m for _, _, m in winners) / len(winners)
    footer(
        f"Average best-in-category margin: {avg_margin:.1f}%.  "
        f"{len(winners)} categories analysed."
    )


# ══════════════════════════════════════════════════════════════════════════════
#  Q3 – Products with no sale in the last 30 days  (datetime.date arithmetic)
# ══════════════════════════════════════════════════════════════════════════════

def q3_stale_inventory(days: int = 30) -> None:
    header(3, f"PRODUCTS WITH NO SALE IN THE LAST {days} DAYS")
    print(f"  Reference date: {TODAY}  │  "
          f"Cutoff: {TODAY - datetime.timedelta(days=days)}\n")

    cutoff = TODAY - datetime.timedelta(days=days)

    # Filter: last_sold_date is strictly before the cutoff
    stale = [p for p in INVENTORY if p["last_sold_date"] < cutoff]
    # Sort oldest-sale-first so the most neglected items appear at the top
    stale.sort(key=lambda p: p["last_sold_date"])

    col = "{:<8} {:<32} {:<14} {:>12} {:>10}"
    print("  " + col.format("SKU", "Product Name", "Category",
                             "Last Sold", "Days Idle"))
    print("  " + "·" * 68)
    for p in stale:
        idle = (TODAY - p["last_sold_date"]).days
        print("  " + col.format(
            p["sku"],
            p["name"][:31],
            p["category"][:13],
            str(p["last_sold_date"]),
            idle
        ))

    total_val = sum(p["cost"] * p["stock_qty"] for p in stale)
    footer(
        f"{len(stale)} stale products found "
        f"({len(stale)/len(INVENTORY)*100:.1f}% of catalogue).  "
        f"Tied-up cost value: ${total_val:,.2f}"
    )


# ══════════════════════════════════════════════════════════════════════════════
#  Q4 – Total inventory value by category  (dict comprehension / defaultdict)
# ══════════════════════════════════════════════════════════════════════════════

def q4_inventory_value_by_category() -> None:
    header(4, "TOTAL INVENTORY VALUE BY CATEGORY (cost × stock_qty)")
    print("  This is the capital currently tied up in each category.\n")

    # Build the aggregation with defaultdict in one readable pass
    cat_value: dict[str, float] = defaultdict(float)
    cat_units: dict[str, int]   = defaultdict(int)
    for p in INVENTORY:
        cat_value[p["category"]] += p["cost"] * p["stock_qty"]
        cat_units[p["category"]] += p["stock_qty"]

    # Sort categories by descending value for quick scanning
    ranked = sorted(cat_value.items(), key=lambda kv: kv[1], reverse=True)
    grand_total = sum(cat_value.values())
    grand_units = sum(cat_units.values())

    col = "{:<14} {:>12} {:>10} {:>9} {:<20}"
    print("  " + col.format("Category", "Inv. Value", "Units",
                             "% Total", "Visual"))
    print("  " + "·" * 68)

    for cat, val in ranked:
        pct = val / grand_total * 100
        bar = "█" * int(pct / 2)          # simple ASCII bar chart
        print("  " + col.format(
            cat[:13],
            f"${val:,.2f}",
            f"{cat_units[cat]:,}",
            f"{pct:.1f}%",
            bar
        ))

    print("  " + "─" * 60)
    print("  " + col.format("TOTAL", f"${grand_total:,.2f}",
                             f"{grand_units:,}", "100.0%", ""))
    footer(
        f"Grand total inventory cost: ${grand_total:,.2f}  │  "
        f"{grand_units:,} units across {len(ranked)} categories."
    )


# ══════════════════════════════════════════════════════════════════════════════
#  Q5 – Top-10 products by projected revenue  (sorted + lambda + slice)
# ══════════════════════════════════════════════════════════════════════════════

def q5_top10_projected_revenue() -> None:
    header(5, "TOP-10 PRODUCTS BY PROJECTED REVENUE (price × stock_qty)")
    print("  Sell every unit on the shelf – this is the gross revenue potential.\n")

    # Sort entire list by projected revenue descending, then slice first 10
    ranked = sorted(
        INVENTORY,
        key=lambda p: p["price"] * p["stock_qty"],
        reverse=True
    )[:10]

    col = "{:<4} {:<8} {:<32} {:<14} {:>8} {:>8} {:>14}"
    print("  " + col.format(
        "Rank", "SKU", "Product Name", "Category",
        "Price", "Qty", "Proj. Revenue"
    ))
    print("  " + "·" * 68)
    for rank, p in enumerate(ranked, start=1):
        rev = p["price"] * p["stock_qty"]
        print("  " + col.format(
            f"#{rank}",
            p["sku"],
            p["name"][:31],
            p["category"][:13],
            f"${p['price']:.2f}",
            p["stock_qty"],
            f"${rev:,.2f}"
        ))

    total_top10 = sum(p["price"] * p["stock_qty"] for p in ranked)
    total_all   = sum(p["price"] * p["stock_qty"] for p in INVENTORY)
    footer(
        f"Top-10 projected revenue: ${total_top10:,.2f}  "
        f"({total_top10/total_all*100:.1f}% of total ${total_all:,.2f})"
    )


# ══════════════════════════════════════════════════════════════════════════════
#  Main entry point
# ══════════════════════════════════════════════════════════════════════════════

def main() -> None:
    print(f"\n{'═'*72}")
    print(f"  INVENTORY INTELLIGENCE REPORT")
    print(f"  Generated : {TODAY}  │  Products analysed: {len(INVENTORY)}")
    print(f"{'═'*72}")

    q1_below_reorder()
    q2_best_margin_per_category()
    q3_stale_inventory(days=30)
    q4_inventory_value_by_category()
    q5_top10_projected_revenue()

    print(f"\n{'═'*72}")
    print("  END OF REPORT")
    print(f"{'═'*72}\n")


if __name__ == "__main__":
    main()