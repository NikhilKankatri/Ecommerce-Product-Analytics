from pathlib import Path

import pandas as pd

# --------------------------------------------------
# 1. LOAD DATASETS
# --------------------------------------------------

PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_DIR / "data" / "raw"

users = pd.read_csv(DATA_DIR / "users.csv", parse_dates=["signup_date"])
events = pd.read_csv(DATA_DIR / "events.csv", parse_dates=["event_timestamp"])
orders = pd.read_csv(DATA_DIR / "orders.csv", parse_dates=["order_date"])
products = pd.read_csv(DATA_DIR / "products.csv")

print("\n========== SHOPSPHERE PRODUCT ANALYTICS ==========")

# --------------------------------------------------
# 2. CONVERSION RATE
# --------------------------------------------------
# Definition:
# Unique users who purchased / unique users who viewed a product * 100

product_viewers = events.loc[
    events["event_name"] == "view_product", "user_id"
].nunique()

purchasers = events.loc[
    events["event_name"] == "purchase", "user_id"
].nunique()

conversion_rate = (
    purchasers / product_viewers * 100
    if product_viewers > 0 else 0
)

print("\n1. CONVERSION RATE")
print(f"Unique product viewers: {product_viewers:,}")
print(f"Unique purchasers: {purchasers:,}")
print(f"Conversion rate: {conversion_rate:.2f}%")

# --------------------------------------------------
# 3. CART ABANDONMENT RATE
# --------------------------------------------------
# Here, we count sessions that added to cart but never purchased.
# This is a simplified session-based metric.

cart_sessions = set(
    events.loc[
        events["event_name"] == "add_to_cart", "session_id"
    ]
)

purchase_sessions = set(
    events.loc[
        events["event_name"] == "purchase", "session_id"
    ]
)

abandoned_sessions = cart_sessions - purchase_sessions

cart_abandonment_rate = (
    len(abandoned_sessions) / len(cart_sessions) * 100
    if cart_sessions else 0
)

print("\n2. CART ABANDONMENT RATE")
print(f"Sessions with add-to-cart: {len(cart_sessions):,}")
print(f"Abandoned cart sessions: {len(abandoned_sessions):,}")
print(f"Cart abandonment rate: {cart_abandonment_rate:.2f}%")

# --------------------------------------------------
# 4. AVERAGE ORDER VALUE (AOV)
# --------------------------------------------------
# AOV = Total revenue / Number of orders

total_revenue = orders["total_amount"].sum()
total_orders = orders["order_id"].nunique()

aov = total_revenue / total_orders if total_orders > 0 else 0

print("\n3. AVERAGE ORDER VALUE")
print(f"Total revenue: ₹{total_revenue:,.2f}")
print(f"Total orders: {total_orders:,}")
print(f"Average order value: ₹{aov:,.2f}")

# --------------------------------------------------
# 5. DAILY ACTIVE USERS (DAU)
# --------------------------------------------------
# For this project, a user is active if they open the app
# or perform a product-related action on that day.

active_events = events[
    events["event_name"].isin([
        "app_open",
        "view_product",
        "add_to_cart",
        "begin_checkout",
        "purchase"
    ])
].copy()

active_events["activity_date"] = (
    active_events["event_timestamp"].dt.date
)

daily_active_users = (
    active_events.groupby("activity_date")["user_id"]
    .nunique()
    .rename("DAU")
)

print("\n4. DAILY ACTIVE USERS")
print(daily_active_users.tail(10).to_string())

# --------------------------------------------------
# 6. MONTHLY ACTIVE USERS (MAU)
# --------------------------------------------------
# MAU = Unique active users in each calendar month.

active_events["activity_month"] = (
    active_events["event_timestamp"].dt.to_period("M")
)

monthly_active_users = (
    active_events.groupby("activity_month")["user_id"]
    .nunique()
    .rename("MAU")
)

print("\n5. MONTHLY ACTIVE USERS")
print(monthly_active_users.to_string())

# --------------------------------------------------
# 7. REVENUE BY ACQUISITION CHANNEL
# --------------------------------------------------

orders_with_users = orders.merge(
    users[["user_id", "acquisition_channel"]],
    on="user_id",
    how="left"
)

revenue_by_channel = (
    orders_with_users.groupby("acquisition_channel")["total_amount"]
    .agg(["sum", "count", "mean"])
    .rename(columns={
        "sum": "total_revenue",
        "count": "number_of_orders",
        "mean": "average_order_value"
    })
    .sort_values("total_revenue", ascending=False)
)

print("\n6. REVENUE BY ACQUISITION CHANNEL")
print(revenue_by_channel.round(2).to_string())

# --------------------------------------------------
# 8. REVENUE BY PRODUCT CATEGORY
# --------------------------------------------------

orders_with_products = orders.merge(
    products[["product_id", "category"]],
    on="product_id",
    how="left"
)

revenue_by_category = (
    orders_with_products.groupby("category")["total_amount"]
    .sum()
    .sort_values(ascending=False)
)

print("\n7. REVENUE BY PRODUCT CATEGORY")
print(revenue_by_category.to_string())

# --------------------------------------------------
# 9. SAVE RESULTS
# --------------------------------------------------

OUTPUT_DIR = PROJECT_DIR / "data" / "cleaned"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

daily_active_users.to_csv(
    OUTPUT_DIR / "daily_active_users.csv"
)

monthly_active_users.to_csv(
    OUTPUT_DIR / "monthly_active_users.csv"
)

revenue_by_channel.to_csv(
    OUTPUT_DIR / "revenue_by_channel.csv"
)

revenue_by_category.to_csv(
    OUTPUT_DIR / "revenue_by_category.csv"
)

print("\nAnalysis completed successfully!")
print(f"Metric files saved in: {OUTPUT_DIR}")