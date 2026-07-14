"""
Retail Sales & Inventory Management — Exploratory Data Analysis
"""
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

plt.rcParams["font.family"] = "DejaVu Sans"
plt.rcParams["axes.spines.top"] = False
plt.rcParams["axes.spines.right"] = False

sales = pd.read_csv("sales_transactions.csv", parse_dates=["date"])
products = pd.read_csv("products.csv")
stores = pd.read_csv("stores.csv")
inventory = pd.read_csv("inventory_weekly_snapshots.csv", parse_dates=["date"])

sales = sales.merge(products, on="product_id").merge(stores, on="store_id")

# ---------------------------------------------------------------
# 1. Monthly revenue trend
# ---------------------------------------------------------------
monthly = sales.groupby(sales["date"].dt.to_period("M"))["total_amount"].sum()
fig, ax = plt.subplots(figsize=(9, 4.5))
monthly.index = monthly.index.astype(str)
ax.plot(monthly.index, monthly.values, marker="o", color="#2563eb", linewidth=2)
ax.fill_between(monthly.index, monthly.values, alpha=0.08, color="#2563eb")
ax.set_title("Monthly Revenue Trend — 2025", fontsize=13, fontweight="bold")
ax.set_ylabel("Revenue (AED)")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x/1000:.0f}K"))
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("chart_monthly_revenue.png", dpi=150)
plt.close()

# ---------------------------------------------------------------
# 2. Revenue by category
# ---------------------------------------------------------------
cat_rev = sales.groupby("category")["total_amount"].sum().sort_values(ascending=True)
fig, ax = plt.subplots(figsize=(8, 4.5))
ax.barh(cat_rev.index, cat_rev.values, color="#0891b2")
ax.set_title("Revenue by Category", fontsize=13, fontweight="bold")
ax.set_xlabel("Revenue (AED)")
ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x/1000:.0f}K"))
plt.tight_layout()
plt.savefig("chart_revenue_by_category.png", dpi=150)
plt.close()

# ---------------------------------------------------------------
# 3. Store performance
# ---------------------------------------------------------------
store_rev = sales.groupby("store_name")["total_amount"].sum().sort_values(ascending=True)
fig, ax = plt.subplots(figsize=(8, 4.5))
ax.barh(store_rev.index, store_rev.values, color="#7c3aed")
ax.set_title("Revenue by Store", fontsize=13, fontweight="bold")
ax.set_xlabel("Revenue (AED)")
ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x/1000:.0f}K"))
plt.tight_layout()
plt.savefig("chart_revenue_by_store.png", dpi=150)
plt.close()

# ---------------------------------------------------------------
# 4. ABC classification (Pareto)
# ---------------------------------------------------------------
prod_rev = sales.groupby("product_name")["total_amount"].sum().sort_values(ascending=False)
cum_pct = prod_rev.cumsum() / prod_rev.sum() * 100
fig, ax1 = plt.subplots(figsize=(10, 4.5))
ax1.bar(range(len(prod_rev)), prod_rev.values, color="#f59e0b")
ax1.set_ylabel("Revenue (AED)")
ax1.set_xticks([])
ax2 = ax1.twinx()
ax2.plot(range(len(prod_rev)), cum_pct.values, color="#dc2626", linewidth=2)
ax2.axhline(80, color="grey", linestyle="--", linewidth=1)
ax2.set_ylabel("Cumulative % of Revenue")
ax1.set_title("ABC / Pareto Analysis — Product Revenue Contribution", fontsize=13, fontweight="bold")
plt.tight_layout()
plt.savefig("chart_abc_pareto.png", dpi=150)
plt.close()

# ---------------------------------------------------------------
# 5. Stockout rate by category
# ---------------------------------------------------------------
inv_prod = inventory.merge(products, on="product_id")
stockout_rate = inv_prod.groupby("category")["stockout_today"].mean().sort_values(ascending=True) * 100
fig, ax = plt.subplots(figsize=(8, 4.5))
ax.barh(stockout_rate.index, stockout_rate.values, color="#dc2626")
ax.set_title("Stockout Rate by Category (% of weeks)", fontsize=13, fontweight="bold")
ax.set_xlabel("Stockout Rate (%)")
plt.tight_layout()
plt.savefig("chart_stockout_rate.png", dpi=150)
plt.close()

# ---------------------------------------------------------------
# Print summary stats for README
# ---------------------------------------------------------------
print("=== SUMMARY ===")
print(f"Total revenue: AED {sales['total_amount'].sum():,.2f}")
print(f"Total transactions: {len(sales):,}")
print(f"Total units sold: {sales['quantity_sold'].sum():,}")
print(f"Avg transaction value: AED {sales['total_amount'].mean():,.2f}")
print(f"Top category: {cat_rev.idxmax()} (AED {cat_rev.max():,.0f})")
print(f"Top store: {store_rev.idxmax()} (AED {store_rev.max():,.0f})")
n_A = (cum_pct <= 80).sum()
print(f"'A' items (top 80% revenue): {n_A} of {len(prod_rev)} products ({n_A/len(prod_rev)*100:.0f}%)")
print(f"Overall stockout rate: {inventory['stockout_today'].mean()*100:.1f}% of store-product-weeks")
print("Charts saved: chart_monthly_revenue.png, chart_revenue_by_category.png,")
print("  chart_revenue_by_store.png, chart_abc_pareto.png, chart_stockout_rate.png")
