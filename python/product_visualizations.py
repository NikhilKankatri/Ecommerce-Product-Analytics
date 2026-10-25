from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

# Locate project folders
PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_DIR / "data" / "raw"
OUTPUT_DIR = PROJECT_DIR / "screenshots"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Load datasets
users = pd.read_csv(DATA_DIR / "users.csv")
events = pd.read_csv(DATA_DIR / "events.csv")
orders = pd.read_csv(DATA_DIR / "orders.csv")
products = pd.read_csv(DATA_DIR / "products.csv")

# --------------------------------------------------
# CHART 1: MONTHLY ACTIVE USERS
# --------------------------------------------------

events["event_timestamp"] = pd.to_datetime(
    events["event_timestamp"]
)

events["activity_month"] = (
    events["event_timestamp"].dt.to_period("M")
)

mau = (
    events.groupby("activity_month")["user_id"]
    .nunique()
)

plt.figure(figsize=(10, 5))
mau.plot(kind="line", marker="o")
plt.title("Monthly Active Users")
plt.xlabel("Month")
plt.ylabel("Unique Active Users")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "monthly_active_users.png")
plt.close()

# --------------------------------------------------
# CHART 2: REVENUE BY ACQUISITION CHANNEL
# --------------------------------------------------

orders_users = orders.merge(
    users[["user_id", "acquisition_channel"]],
    on="user_id",
    how="left"
)

channel_revenue = (
    orders_users.groupby("acquisition_channel")["total_amount"]
    .sum()
    .sort_values(ascending=False)
)

plt.figure(figsize=(9, 5))
channel_revenue.plot(kind="bar")
plt.title("Revenue by Acquisition Channel")
plt.xlabel("Acquisition Channel")
plt.ylabel("Revenue")
plt.xticks(rotation=30)
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "revenue_by_channel.png")
plt.close()

# --------------------------------------------------
# CHART 3: REVENUE BY PRODUCT CATEGORY
# --------------------------------------------------

orders_products = orders.merge(
    products[["product_id", "category"]],
    on="product_id",
    how="left"
)

category_revenue = (
    orders_products.groupby("category")["total_amount"]
    .sum()
    .sort_values(ascending=False)
)

plt.figure(figsize=(9, 5))
category_revenue.plot(kind="bar")
plt.title("Revenue by Product Category")
plt.xlabel("Product Category")
plt.ylabel("Revenue")
plt.xticks(rotation=30)
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "revenue_by_category.png")
plt.close()

# --------------------------------------------------
# CHART 4: CONVERSION FUNNEL
# --------------------------------------------------

event_counts = events.groupby("event_name")["user_id"].nunique()

funnel_stages = [
    "app_open",
    "view_product",
    "add_to_cart",
    "begin_checkout",
    "purchase"
]

funnel_values = [
    int(event_counts.get(stage, 0))
    for stage in funnel_stages
]

plt.figure(figsize=(10, 5))
plt.barh(funnel_stages, funnel_values)
plt.title("E-Commerce User Conversion Funnel")
plt.xlabel("Unique Users")
plt.ylabel("Event")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "conversion_funnel.png")
plt.close()

print("All four charts created successfully!")
print(f"Charts saved in: {OUTPUT_DIR}")