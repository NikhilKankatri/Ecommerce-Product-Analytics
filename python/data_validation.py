from pathlib import Path

import pandas as pd

# Locate the project and dataset folders
PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_DIR / "data" / "raw"

# Load all datasets
users = pd.read_csv(DATA_DIR / "users.csv")
products = pd.read_csv(DATA_DIR / "products.csv")
events = pd.read_csv(DATA_DIR / "events.csv")
orders = pd.read_csv(DATA_DIR / "orders.csv")
experiments = pd.read_csv(DATA_DIR / "experiments.csv")

datasets = {
    "Users": users,
    "Products": products,
    "Events": events,
    "Orders": orders,
    "Experiments": experiments
}

# 1. Dataset sizes
print("\n========== DATASET SIZES ==========")

for name, df in datasets.items():
    print(f"{name}: {len(df):,} rows and {len(df.columns)} columns")

# 2. Missing values
print("\n========== MISSING VALUES ==========")

for name, df in datasets.items():
    missing = df.isnull().sum().sum()
    print(f"{name}: {missing} missing values")

# 3. Duplicate records
print("\n========== DUPLICATE RECORDS ==========")

for name, df in datasets.items():
    duplicates = df.duplicated().sum()
    print(f"{name}: {duplicates} duplicate rows")

# 4. Unique users and products
print("\n========== UNIQUE COUNTS ==========")

print("Unique users:", users["user_id"].nunique())
print("Unique products:", products["product_id"].nunique())
print("Unique event IDs:", events["event_id"].nunique())
print("Unique orders:", orders["order_id"].nunique())

# 5. Event breakdown
print("\n========== EVENT BREAKDOWN ==========")

print(events["event_name"].value_counts())

# 6. Revenue summary
print("\n========== REVENUE SUMMARY ==========")

print("Total orders:", len(orders))
print("Total revenue:", round(orders["total_amount"].sum(), 2))

if len(orders) > 0:
    print(
        "Average order value:",
        round(orders["total_amount"].mean(), 2)
    )
else:
    print("Average order value: No orders yet")

# 7. Check invalid user references
print("\n========== DATA CONSISTENCY ==========")

invalid_event_users = (
    ~events["user_id"].isin(users["user_id"])
).sum()

invalid_order_users = (
    ~orders["user_id"].isin(users["user_id"])
).sum()

invalid_event_products = (
    ~events["product_id"].isin(products["product_id"])
).sum()

invalid_order_products = (
    ~orders["product_id"].isin(products["product_id"])
).sum()

print("Events with unknown users:", invalid_event_users)
print("Orders with unknown users:", invalid_order_users)
print("Events with unknown products:", invalid_event_products)
print("Orders with unknown products:", invalid_order_products)

print("\nData validation completed!")