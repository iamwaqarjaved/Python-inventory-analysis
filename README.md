# Inventory Analyser 📦

A Python CLI tool that loads 196 product records and answers 5 real business questions:

1. **Reorder alerts** – which products are below their reorder point?
2. **Best margin** – highest-margin product in each category
3. **Stale stock** – products with no sale in the last 30 days
4. **Inventory value** – total cost × qty breakdown by category
5. **Revenue potential** – top-10 products by price × stock qty

## How to run

```bash
python3 analyzer.py
```

## Files

| File | Purpose |
|------|---------|
| `inventory.py` | Dataset – 196 products, 15 categories |
| `analyzer.py`  | Report engine – answers all 5 questions |

## Requirements

Python 3.8 or later. No third-party libraries needed.
EOF
