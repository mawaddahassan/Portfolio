# Retail Sales & Inventory Management Analytics

End-to-end analytics project on a simulated multi-store retail business: transaction-level sales, product catalog, and weekly inventory tracking across five stores and 40 SKUs over FY2025. Built to demonstrate SQL analysis, Excel dashboarding, and Python EDA on a realistic retail dataset.

## Business context

A mid-size retailer with 4 physical stores and 1 online channel wants to understand:
- Where revenue and profit are coming from (by category, product, store, time)
- Which products deserve tighter inventory control (ABC/Pareto analysis)
- Which store-product combinations are at risk of stockouts and need a purchase order
- How seasonality and promotions affect demand

## Dataset

Synthetic but realistic data generated with a day-by-day simulation (`generate_data.py`) that models seasonality (holiday peaks, summer dip, weekend lift), promotional discounts, product popularity, and a working reorder-point/lead-time replenishment system — including occasional supplier delays and demand spikes that produce genuine stockouts.

| File | Description | Rows |
|---|---|---|
| `sales_transactions.csv` | Line-item sales: date, store, product, quantity, price, discount, total | 33,604 |
| `inventory_weekly_snapshots.csv` | Weekly stock-on-hand, reorder point, stockout flag per store/product | 10,400 |
| `products.csv` | 40 SKUs across 4 categories, with cost, price, reorder point/qty, supplier, lead time | 40 |
| `stores.csv` | 5 stores (4 physical + 1 online) with region and store type | 5 |

**Key figures:** AED 12,173,997 total revenue · 33,604 transactions · 63,175 units sold · 10.4% of store-product-weeks experienced a stockout.

## Project structure

```
├── generate_data.py                          # synthetic data generator
├── sales_transactions.csv
├── inventory_weekly_snapshots.csv
├── products.csv
├── stores.csv
├── retail.db                                 # SQLite DB (same 4 tables, ready to query)
├── sql_analysis.sql                          # 10 business-question SQL queries
├── eda_analysis.py                           # Python EDA — generates the charts below
├── charts/
│   ├── chart_monthly_revenue.png
│   ├── chart_revenue_by_category.png
│   ├── chart_revenue_by_store.png
│   ├── chart_abc_pareto.png
│   └── chart_stockout_rate.png
|
└── Retail_Sales_Inventory_Dashboard.xlsx      # interactive Excel dashboard
```

## Analysis 1 — SQL (`sql_analysis.sql`, runs against `retail.db`)

10 queries answering concrete business questions:
1. Monthly revenue, units, and transaction count
2. Revenue and gross margin by category
3. Top 10 products by revenue
4. Store performance ranking (revenue, average basket size)
5. ABC/Pareto classification of every product
6. Stockout frequency by product
7. Store-product combinations currently at/below reorder point
8. Month-over-month revenue growth %
9. Discount vs full-price transaction comparison
10. Weekday vs weekend sales pattern

Load it with:
```bash
sqlite3 retail.db < sql_analysis.sql
```

## Analysis 2 — Excel Dashboard (`Retail_Sales_Inventory_Dashboard.xlsx`)

A fully formula-driven workbook (no hardcoded results — everything recalculates from the raw data tabs):

- **Dashboard** tab: 5 KPI cards, monthly revenue line chart, category revenue/margin bar chart, top 10 products table, store performance table, and a live reorder-alert table flagging every store-product combination at or below its reorder point
- **ABC_Analysis** tab: full product-level Pareto ranking with A/B/C classification
- **Raw_Sales / Raw_Products / Raw_Stores / Raw_Inventory** tabs: the underlying data as native Excel tables

## Analysis 3 — Python EDA (`eda_analysis.py`)

Generates the five charts below using `pandas` + `matplotlib`.

### Key findings

**Revenue is strongly seasonal.** November and December each brought in roughly 40-50% more revenue than the mid-year low points (June/July), driven by the Black Friday and year-end sale periods built into the simulation.

**Product revenue is concentrated.** In this dataset, roughly half of the 40 SKUs (the "A" class) account for 80% of total revenue — a textbook Pareto pattern that argues for tighter inventory control on a relatively small set of fast-movers rather than spreading effort evenly across the catalog.

**Stockouts cluster around high-demand SKUs.** 10.4% of store-product-weeks recorded at least one stockout day, concentrated in categories with the highest demand variability — evidence that reorder points calibrated for average demand aren't enough to protect against demand spikes and occasional supplier delays.

**Discount transactions move more units per basket** than full-price transactions, consistent with promotions successfully driving incremental volume rather than just margin erosion.

## Tools used

- **Python** (pandas, numpy, matplotlib) — data generation and EDA
- **SQL** (SQLite) — business-question queries, window functions (running totals, LAG for MoM growth)
- **Excel** (openpyxl) — formula-driven interactive dashboard with native charts

## How to reproduce

```bash
pip install pandas numpy matplotlib openpyxl
python generate_data.py      # regenerates the 4 CSVs
python eda_analysis.py       # regenerates the 5 PNG charts
python build_excel.py        # rebuilds the Excel dashboard
sqlite3 retail.db < sql_analysis.sql   # runs the SQL queries
```

---
*This is a self-directed portfolio project built on a synthetic dataset to demonstrate data analysis skills across SQL, Excel, and Python.*
