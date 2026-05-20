# 📦 Python Inventory Analysis

> **Practise core Python data structures by answering 5 real business questions on a 196-product inventory dataset — no external libraries required.**

[![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?style=flat&logo=python&logoColor=white)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-22c55e?style=flat)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Complete-22c55e?style=flat)]()
[![Beginner Friendly](https://img.shields.io/badge/Level-Beginner%20Friendly-6366f1?style=flat)]()

---

## 🗂️ Table of Contents

1. [Project Overview](#-project-overview)
2. [What the Analyser Does](#-what-the-analyser-does)
3. [Project Structure](#-project-structure)
4. [Prerequisites](#-prerequisites)
5. [Quick Start](#-quick-start)
6. [Sample Output](#-sample-output)
7. [Data Structure Choices Explained](#-data-structure-choices-explained)
8. [Concepts Covered](#-concepts-covered)
9. [Extend This Project](#-extend-this-project)
10. [Contributing](#-contributing)
11. [Author](#-author)
12. [License](#-license)

---

## 🔍 Project Overview

This project is a **command-line inventory intelligence tool** written in pure Python. It loads a realistic dataset of 196 products across 15 categories (Electronics, Furniture, Office Supplies, Cleaning, and more) and produces a formatted business report answering five critical operational questions a store owner or supply-chain analyst would ask every day.

The goal is not just to get answers — it is to choose the **right data structure for each operation** and understand *why* that choice matters for readability, correctness, and performance.

**Perfect for:**
- 🎓 Students working through Python data-structure labs
- 💼 Developers building portfolio projects
- 🏪 Anyone learning how Python can solve real retail/inventory problems

---

## 📊 What the Analyser Does

The `analyzer.py` script answers **5 business questions** from the dataset:

| # | Business Question | Python Technique |
|---|-------------------|-----------------|
| 1 | Which 10 products are below their reorder point? | `list` comprehension → `.sort()` with `lambda` → slice |
| 2 | Which product in each category has the highest profit margin? | `defaultdict(list)` group-by → `max()` with `lambda` |
| 3 | Which products have not sold in the last 30 days? | `datetime.timedelta` arithmetic → `list` filter |
| 4 | What is total inventory value (cost × qty) per category? | `defaultdict(float)` aggregation → ranked `sorted()` |
| 5 | What are the top-10 products by projected revenue (price × qty)? | `sorted()` with `key=lambda` → slice `[:10]` |

Each question prints a **clean, aligned table** with a summary line — output you could copy straight into a report or email.

---

## 🗃️ Project Structure

```
Python-inventory-analysis/
│
├── inventory.py        # Dataset — 196 products, 15 categories, 8 fields each
├── analyzer.py         # Report engine — answers all 5 questions
├── README.md           # This file
└── .gitignore          # Excludes __pycache__, .DS_Store, report.txt
```

### Dataset fields (per product)

| Field | Type | Description |
|-------|------|-------------|
| `sku` | `str` | Unique stock-keeping unit code |
| `name` | `str` | Human-readable product name |
| `category` | `str` | Product category (15 categories) |
| `price` | `float` | Retail selling price (USD) |
| `cost` | `float` | Unit purchase / cost price (USD) |
| `stock_qty` | `int` | Units currently on the shelf |
| `reorder_point` | `int` | Minimum stock level before reorder |
| `last_sold_date` | `datetime.date` | Date of the most recent sale |

---

## ✅ Prerequisites

- **Python 3.8 or later** — that is all. No `pip install` needed.
- A terminal (macOS Terminal, Windows Command Prompt / PowerShell, or Linux shell)

Check your Python version:

```bash
python3 --version
```

If you see `Python 3.x.x` you are ready to go. If Python is not installed, see the [installation guide](https://www.python.org/downloads/).

---

## 🚀 Quick Start

### 1 — Clone the repository

```bash
git clone https://github.com/iamwaqarjaved/Python-inventory-analysis.git
```

### 2 — Enter the project folder

```bash
cd Python-inventory-analysis
```

### 3 — Run the analyser

```bash
python3 analyzer.py
```

The full five-question report prints immediately in your terminal.

### 4 — Save the report to a file (optional)

```bash
python3 analyzer.py > report.txt
```

---

## 🖥️ Sample Output

```
════════════════════════════════════════════════════════════════════════
  INVENTORY INTELLIGENCE REPORT
  Generated : 2026-05-19  │  Products analysed: 196
════════════════════════════════════════════════════════════════════════

════════════════════════════════════════════════════════════════════════
  Q1  │  TOP-10 PRODUCTS BELOW REORDER POINT
════════════════════════════════════════════════════════════════════════
  These items need restocking before they run out of stock.

SKU      Product Name                     Category        In Stock   Reorder At  Shortfall
  ····································································
  OF002    A4 Copy Paper 500 sheets         Office                18           50        –32
  EL010    Smart Power Strip                Electronics            5           20        –15
  CL012    Latex Gloves M 100pk             Cleaning              15           30        –15
  ...

════════════════════════════════════════════════════════════════════════
  Q4  │  TOTAL INVENTORY VALUE BY CATEGORY (cost × stock_qty)
════════════════════════════════════════════════════════════════════════

  Category         Inv. Value      Units   % Total Visual
  ····································································
  Electronics      $21,700.00      1,406     25.0% ████████████
  Furniture        $13,806.00        166     15.9% ███████
  Office            $6,640.80      1,736      7.7% ███
  ...
  ──────────────────────────────────────────────────────────
  TOTAL            $86,783.10     10,258    100.0%

════════════════════════════════════════════════════════════════════════
  END OF REPORT
════════════════════════════════════════════════════════════════════════
```

---

## 🧠 Data Structure Choices Explained

A core objective of this project is to justify *why* each data structure was selected — not just *that* it works.

### Q1 — List comprehension + in-place sort

A **list comprehension** filters in one readable pass (O(n)). In-place `.sort()` is used — not `sorted()` — because we own the filtered list and have no need to preserve its original order. The `key=lambda` computes the shortfall inline without storing an extra field.

### Q2 — `defaultdict(list)` for group-by

`defaultdict(list)` eliminates the `if key not in dict` boilerplate. `max()` with a `key=` lambda finds the best margin per group in O(k) — cheaper than sorting (O(k log k)) when only one extreme value is needed.

### Q3 — `datetime.timedelta` for date arithmetic

Comparing dates as `datetime.date` objects (not strings) ensures correct month and year boundary handling. Subtracting a `timedelta(days=30)` from `date.today()` gives an exact cutoff in one expression.

### Q4 — `defaultdict(float)` for aggregation

Two `defaultdict`s (`float` for value, `int` for units) accumulate totals in a single O(n) pass. No pre-scan for unique categories is needed because `defaultdict` initialises missing keys automatically.

### Q5 — `sorted()` + slice

`sorted()` (not `.sort()`) returns a **new** list, leaving `INVENTORY` unchanged for other questions in the same run. The `key=lambda` computes `price × stock_qty` without mutating any dict. The summary total uses a **generator expression** — memory-efficient for large datasets.

---

## 📚 Concepts Covered

```
✔ List comprehensions and filtering
✔ Lambda functions as sort keys
✔ defaultdict from the collections module
✔ max() and sorted() with custom key functions
✔ datetime.date and datetime.timedelta arithmetic
✔ Dictionary grouping (group-by pattern)
✔ Generator expressions vs list comprehensions
✔ f-strings and formatted console output
✔ Module imports (inventory.py → analyzer.py)
✔ Pure-Python scripting — zero external dependencies
```

---

## 🔧 Extend This Project

Here are ideas for taking this further:

| Extension | Hint |
|-----------|------|
| **Q6 — Low turnover alert** | Combine Q3 (stale) with Q1 (below reorder) |
| **Export to CSV** | `import csv` and `csv.DictWriter` |
| **Interactive menu** | Wrap each question in a `while True` loop |
| **Load from a real CSV** | Replace the `INVENTORY` list with `csv.reader` |
| **Add a margin threshold filter** | Accept a `--min-margin` CLI argument via `argparse` |
| **Matplotlib bar chart** | Visualise Q4 category values as a bar chart |
| **Unit tests** | Write `pytest` tests for each analyser function |

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Commit your changes: `git commit -m "Add: your feature description"`
4. Push to your fork: `git push origin feature/your-feature-name`
5. Open a Pull Request

Please keep pull requests focused — one feature or fix per PR.

---

## 👤 Author

**Waqar Javed**

- GitHub: [@iamwaqarjaved](https://github.com/iamwaqarjaved)

If this project helped you, please consider leaving a ⭐ — it helps others find it!

---

## 📄 License

This project is released under the [MIT License](LICENSE) — free to use, modify, and distribute with attribution.

---

*Built with Python 3 · No external dependencies · Beginner friendly*