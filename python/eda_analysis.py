# Step 15: Exploratory Data Analysis (EDA)
# Purpose: Explore the ShopSphere e-commerce dataset.
# Business Objective: Understand user behavior, product performance,
# and revenue trends.

import matplotlib.pyplot as plt
import pandas as pd

# Load datasets
users = pd.read_csv("data/raw/users.csv")
events = pd.read_csv("data/raw/events.csv")
products = pd.read_csv("data/raw/products.csv")
orders = pd.read_csv("data/raw/orders.csv")

# 1. Display dataset dimensions
print("\n--- Dataset Shapes ---")
print("Users:", users.shape)
print("Events:", events.shape)
print("Products:", products.shape)
print("Orders:", orders.shape)

# 2. Check missing values
print("\n--- Missing Values ---")
print("Users:\n", users.isnull().sum())
print("\nEvents:\n", events.isnull().sum())
print("\nProducts:\n", products.isnull().sum())
print("\nOrders:\n", orders.isnull().sum())

# 3. Check duplicate records
print("\n--- Duplicate Records ---")
print("Duplicate users:", users.duplicated().sum())
print("Duplicate events:", events.duplicated().sum())
print("Duplicate products:", products.duplicated().sum())
print("Duplicate orders:", orders.duplicated().sum())

# 4. Analyze event types
print("\n--- Event Counts ---")
print(events["event_name"].value_counts())

# 5. Analyze revenue by product category
revenue_by_category = (
    orders.merge(products, on="product_id", how="left")
    .groupby("category")["total_amount"]
    .sum()
    .sort_values(ascending=False)
)

print("\n--- Revenue by Category ---")
print(revenue_by_category)

# 6. Visualize revenue by category
revenue_by_category.plot(kind="bar", title="Revenue by Product Category")
plt.xlabel("Product Category")
plt.ylabel("Revenue")
plt.tight_layout()
plt.savefig("screenshots/python_revenue_by_category.png")
plt.show()

print("\nEDA analysis completed successfully!")