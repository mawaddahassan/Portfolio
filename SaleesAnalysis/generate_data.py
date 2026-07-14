"""
Generate a synthetic Retail Sales & Inventory Management dataset.
Simulates 1 year of transactions across 5 stores and 40 products,
with realistic seasonality, promotions, stockouts, and replenishment.
"""
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

np.random.seed(42)

# ---------------------------------------------------------------
# 1. DIMENSION TABLES
# ---------------------------------------------------------------

stores = pd.DataFrame([
    {"store_id": "ST01", "store_name": "Downtown Flagship", "region": "Central", "city": "Dubai", "store_type": "Flagship"},
    {"store_id": "ST02", "store_name": "Mall Branch North",  "region": "North",   "city": "Sharjah", "store_type": "Mall"},
    {"store_id": "ST03", "store_name": "Mall Branch South",  "region": "South",   "city": "Abu Dhabi", "store_type": "Mall"},
    {"store_id": "ST04", "store_name": "Suburban Outlet",    "region": "West",    "city": "Ajman", "store_type": "Outlet"},
    {"store_id": "ST05", "store_name": "Online Fulfillment", "region": "Online",  "city": "N/A", "store_type": "Online"},
])

categories = {
    "Electronics":   ["Wireless Earbuds", "Bluetooth Speaker", "Smart Watch", "Phone Charger", "USB-C Cable",
                       "Power Bank", "Laptop Sleeve", "Wireless Mouse", "Webcam HD", "Screen Protector"],
    "Home & Kitchen": ["Ceramic Mug Set", "Non-Stick Pan", "Electric Kettle", "Blender", "Cutlery Set",
                        "Storage Containers", "Table Lamp", "Throw Pillow", "Bath Towel Set", "Air Freshener"],
    "Apparel":        ["Cotton T-Shirt", "Denim Jeans", "Running Shoes", "Wool Sweater", "Baseball Cap",
                        "Leather Belt", "Rain Jacket", "Sports Socks", "Sunglasses", "Backpack"],
    "Beauty & Personal Care": ["Face Moisturizer", "Shampoo 500ml", "Sunscreen SPF50", "Lip Balm Set", "Hair Dryer",
                                "Electric Toothbrush", "Perfume 100ml", "Body Lotion", "Nail Care Kit", "Makeup Brush Set"],
}

product_rows = []
pid = 1
for cat, items in categories.items():
    for name in items:
        base_cost = np.round(np.random.uniform(15, 220), 2)
        margin = np.random.uniform(1.35, 2.1)
        product_rows.append({
            "product_id": f"P{pid:03d}",
            "product_name": name,
            "category": cat,
            "unit_cost": base_cost,
            "unit_price": np.round(base_cost * margin, 2),
            "reorder_point": int(np.random.randint(6, 18)),
            "reorder_qty": int(np.random.randint(25, 70)),
            "supplier": f"Supplier {chr(65 + (pid % 6))}",
            "lead_time_days": int(np.random.choice([3, 5, 7, 10, 14])),
        })
        pid += 1
products = pd.DataFrame(product_rows)

# Popularity weight per product (some products sell much more than others)
products["popularity"] = np.random.gamma(shape=2.0, scale=1.0, size=len(products))

stores.to_csv("stores.csv", index=False)
products.drop(columns=["popularity"]).to_csv("products.csv", index=False)

# ---------------------------------------------------------------
# 2. DATE RANGE + SEASONALITY
# ---------------------------------------------------------------
start_date = datetime(2025, 1, 1)
end_date = datetime(2025, 12, 31)
date_range = pd.date_range(start_date, end_date, freq="D")

def seasonal_factor(date):
    # Ramadan-style spring dip + big Nov/Dec (Black Friday/holiday) boost + summer dip
    month = date.month
    factor = 1.0
    if month in (11, 12):
        factor *= 1.55
    if month in (6, 7):
        factor *= 0.82
    if date.weekday() >= 4:  # Fri/Sat/Sun busier
        factor *= 1.25
    # Black Friday spike (last Friday of Nov) + year-end sale
    if date.month == 11 and 24 <= date.day <= 30:
        factor *= 1.6
    if date.month == 12 and 20 <= date.day <= 31:
        factor *= 1.3
    return factor

store_weight = {"ST01": 1.4, "ST02": 1.1, "ST03": 1.0, "ST04": 0.7, "ST05": 1.3}

# ---------------------------------------------------------------
# 3. SIMULATE INVENTORY + SALES DAY BY DAY (per store/product)
# ---------------------------------------------------------------
inventory_state = {}
for s in stores["store_id"]:
    for _, p in products.iterrows():
        inventory_state[(s, p["product_id"])] = int(np.random.randint(p["reorder_point"], p["reorder_point"] + int(p["reorder_qty"] * 0.6)))

sales_rows = []
inventory_rows = []
sale_id = 1
pending_orders = {}  # (store, product) -> list of (arrival_date, qty)
weekly_stockout_days = {}  # (store, product) -> count of stockout days so far this week

for date in date_range:
    sf = seasonal_factor(date)
    for _, p in products.iterrows():
        for s in stores["store_id"]:
            key = (s, p["product_id"])

            # receive any pending purchase orders arriving today
            if key in pending_orders:
                still_pending = []
                for arrival, qty in pending_orders[key]:
                    if arrival <= date:
                        inventory_state[key] += qty
                    else:
                        still_pending.append((arrival, qty))
                pending_orders[key] = still_pending

            # expected daily demand (with occasional demand spikes to stress-test inventory)
            lam = 0.32 * p["popularity"] * store_weight[s] * sf
            if np.random.random() < 0.07:
                lam *= np.random.uniform(3.0, 6.0)  # viral/promo spike
            demand = np.random.poisson(lam=max(lam, 0.01))

            on_hand = inventory_state[key]
            sold = min(demand, on_hand)
            stockout = demand > on_hand

            if sold > 0:
                # occasional promotional discount
                discount = np.random.choice([0, 0, 0, 0.10, 0.15, 0.20], p=[0.7, 0.08, 0.07, 0.06, 0.05, 0.04])
                unit_price = p["unit_price"]
                total = round(sold * unit_price * (1 - discount), 2)
                sales_rows.append({
                    "sale_id": f"SL{sale_id:07d}",
                    "date": date.strftime("%Y-%m-%d"),
                    "store_id": s,
                    "product_id": p["product_id"],
                    "quantity_sold": sold,
                    "unit_price": unit_price,
                    "discount_pct": discount,
                    "total_amount": total,
                })
                sale_id += 1

            inventory_state[key] = on_hand - sold

            if stockout:
                weekly_stockout_days[key] = weekly_stockout_days.get(key, 0) + 1

            # reorder logic: if stock falls at/below reorder point, place PO (arrives after lead_time)
            already_pending = key in pending_orders and len(pending_orders[key]) > 0
            if inventory_state[key] <= p["reorder_point"] and not already_pending:
                lead = int(p["lead_time_days"])
                if np.random.random() < 0.12:
                    lead += int(np.random.randint(5, 12))  # occasional supplier delay
                arrival = date + timedelta(days=lead)
                pending_orders.setdefault(key, []).append((arrival, int(p["reorder_qty"])))

            # log weekly inventory snapshot (Sundays) to keep file size manageable
            if date.weekday() == 6:
                inventory_rows.append({
                    "date": date.strftime("%Y-%m-%d"),
                    "store_id": s,
                    "product_id": p["product_id"],
                    "stock_on_hand": inventory_state[key],
                    "reorder_point": p["reorder_point"],
                    "stockout_days_this_week": weekly_stockout_days.get(key, 0),
                    "stockout_today": weekly_stockout_days.get(key, 0) > 0,
                })
                weekly_stockout_days[key] = 0

sales = pd.DataFrame(sales_rows)
inventory_snapshots = pd.DataFrame(inventory_rows)

sales.to_csv("sales_transactions.csv", index=False)
inventory_snapshots.to_csv("inventory_weekly_snapshots.csv", index=False)

print("Products:", len(products))
print("Stores:", len(stores))
print("Sales transactions:", len(sales))
print("Inventory snapshot rows:", len(inventory_snapshots))
print("Date range:", start_date.date(), "to", end_date.date())
print("Total revenue: AED", round(sales["total_amount"].sum(), 2))
