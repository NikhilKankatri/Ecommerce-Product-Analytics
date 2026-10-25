# Step 18: Revenue and Product Performance Analysis
# Purpose: Analyze revenue by product, category, and acquisition channel.
# Business Objective: Identify high-performing products and revenue sources.

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

# Define project paths
PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_DIR / "data" / "cleaned"
RAW_DIR = PROJECT_DIR / "data" / "raw"
OUTPUT_DIR = PROJECT_DIR / "screenshots"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Load datasets
orders = pd.read_csv(DATA_DIR / "orders_cleaned.csv")
products = pd.read_csv(DATA_DIR / "products_cleaned.csv")
users = pd.read_csv(DATA_DIR / "users_cleaned.csv")

# Join orders with product and user information
sales = orders.merge(products, on="product_id", how="left")
sales = sales.merge(
    users[["user_id", "acquisition_channel"]],
    on="user_id",
    how="left"
)

# 1. Overall business KPIs
total_revenue = sales["total_amount"].sum()
total_orders = sales["order_id"].nunique()
total_customers = sales["user_id"].nunique()
average_order_value = total_revenue / total_orders if total_orders else 0

print("\n--- OVERALL BUSINESS KPIs ---")
print(f"Total Revenue: ₹{total_revenue:,.2f}")
print(f"Total Orders: {total_orders:,}")
print(f"Unique Purchasing Customers: {total_customers:,}")
print(f"Average Order Value: ₹{average_order_value:,.2f}")

# 2. Revenue by product category
category_revenue = (
    sales.groupby("category")["total_amount"]
    .sum()
    .sort_values(ascending=False)
)

print("\n--- REVENUE BY CATEGORY ---")
print(category_revenue.to_string())

# 3. Revenue by product
product_revenue = (
    sales.groupby("product_name")
    .agg(
        revenue=("total_amount", "sum"),
        orders=("order_id", "nunique"),
        quantity_sold=("quantity", "sum")
    )
    .sort_values("revenue", ascending=False)
)

print("\n--- TOP 10 PRODUCTS BY REVENUE ---")
print(product_revenue.head(10).to_string())

# 4. Revenue by acquisition channel
channel_revenue = (
    sales.groupby("acquisition_channel")
    .agg(
        revenue=("total_amount", "sum"),
        orders=("order_id", "nunique"),
        customers=("user_id", "nunique")
    )
    .sort_values("revenue", ascending=False)
)

print("\n--- REVENUE BY ACQUISITION CHANNEL ---")
print(channel_revenue.to_string())

# 5. Plot revenue by category
category_revenue.plot(kind="bar", title="Revenue by Product Category")
plt.xlabel("Category")
plt.ylabel("Revenue")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "revenue_by_category_python.png", dpi=150)
plt.show()

# 6. Plot revenue by acquisition channel
channel_revenue["revenue"].plot(
    kind="bar",
    title="Revenue by Acquisition Channel"
)
plt.xlabel("Acquisition Channel")
plt.ylabel("Revenue")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "revenue_by_channel_python.png", dpi=150)
plt.show()

# 7. Export analysis results
category_revenue.to_csv(OUTPUT_DIR / "category_revenue.csv")
product_revenue.to_csv(OUTPUT_DIR / "product_revenue.csv")
channel_revenue.to_csv(OUTPUT_DIR / "channel_revenue.csv")

print("\nAnalysis completed successfully!")
print("Charts and CSV reports saved in the screenshots folder.")