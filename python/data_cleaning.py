# Step 16: Data Cleaning Using Python
# Purpose: Clean and validate e-commerce datasets.
# Business Objective: Improve data quality before analysis.

from pathlib import Path

import pandas as pd

# Set project directories
PROJECT_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = PROJECT_DIR / "data" / "raw"
CLEAN_DIR = PROJECT_DIR / "data" / "cleaned"

# Create the cleaned data folder if it doesn't exist
CLEAN_DIR.mkdir(parents=True, exist_ok=True)

# Load raw datasets
users = pd.read_csv(RAW_DIR / "users.csv")
events = pd.read_csv(RAW_DIR / "events.csv")
products = pd.read_csv(RAW_DIR / "products.csv")
orders = pd.read_csv(RAW_DIR / "orders.csv")

# 1. Convert date columns to the correct format
users["signup_date"] = pd.to_datetime(
    users["signup_date"], errors="coerce"
)

events["event_timestamp"] = pd.to_datetime(
    events["event_timestamp"], errors="coerce"
)

orders["order_date"] = pd.to_datetime(
    orders["order_date"], errors="coerce"
)

# 2. Remove duplicate records based on unique IDs
users = users.drop_duplicates(subset=["user_id"])
events = events.drop_duplicates(subset=["event_id"])
products = products.drop_duplicates(subset=["product_id"])
orders = orders.drop_duplicates(subset=["order_id"])

# 3. Remove records missing essential information
users = users.dropna(
    subset=["user_id", "signup_date"]
)

events = events.dropna(
    subset=["event_id", "user_id", "event_timestamp", "event_name"]
)

products = products.dropna(
    subset=["product_id", "product_name", "price"]
)

orders = orders.dropna(
    subset=["order_id", "user_id", "product_id", "order_date",
            "quantity", "total_amount"]
)

# 4. Keep only records with valid positive prices and order values
products = products[products["price"] > 0]

orders = orders[
    (orders["quantity"] > 0) &
    (orders["total_amount"] > 0)
]

# 5. Validate relationships between datasets
valid_user_ids = set(users["user_id"])
valid_product_ids = set(products["product_id"])

# Keep valid users and retain events without a product ID.
# Validate the product ID only when one is provided.

events = events[
    events["user_id"].isin(valid_user_ids)
    & (
        events["product_id"].isna()
        | events["product_id"].isin(valid_product_ids)
    )
]

orders = orders[
    orders["user_id"].isin(valid_user_ids)
    & orders["product_id"].isin(valid_product_ids)
]

# 6. Save cleaned datasets
users.to_csv(CLEAN_DIR / "users_cleaned.csv", index=False)
events.to_csv(CLEAN_DIR / "events_cleaned.csv", index=False)
products.to_csv(CLEAN_DIR / "products_cleaned.csv", index=False)
orders.to_csv(CLEAN_DIR / "orders_cleaned.csv", index=False)

# 7. Display cleaning summary
print("\n--- DATA CLEANING SUMMARY ---")

print("Users:", len(users))
print("Events:", len(events))
print("Products:", len(products))
print("Orders:", len(orders))

print("\nCleaned datasets saved to:", CLEAN_DIR)
print("Data cleaning completed successfully!")