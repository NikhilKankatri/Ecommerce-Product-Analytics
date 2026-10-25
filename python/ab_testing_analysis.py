# Step 20: A/B Testing Analysis Using Python
# Purpose: Compare conversion rates between two experiment groups.
# Group A: Control group.
# Group B: Variant group.
# Business Objective: Evaluate checkout experiment performance.

import math
from pathlib import Path

import pandas as pd

# Define project paths
PROJECT_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = PROJECT_DIR / "data" / "raw"
CLEAN_DIR = PROJECT_DIR / "data" / "cleaned"
OUTPUT_DIR = PROJECT_DIR / "screenshots"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Load datasets
experiments = pd.read_csv(RAW_DIR / "experiments.csv")
orders = pd.read_csv(CLEAN_DIR / "orders_cleaned.csv")

# Convert dates
experiments["assignment_timestamp"] = pd.to_datetime(
    experiments["assignment_timestamp"], errors="coerce"
).dt.date

orders["order_date"] = pd.to_datetime(
    orders["order_date"], errors="coerce"
).dt.date

# Keep orders placed on or after experiment assignment
eligible_orders = orders.merge(
    experiments[["user_id", "assignment_timestamp"]],
    on="user_id",
    how="inner"
)

eligible_orders = eligible_orders[
    eligible_orders["order_date"]
    >= eligible_orders["assignment_timestamp"]
]

# Identify users who converted after assignment
converted_users = set(eligible_orders["user_id"].unique())

experiments["actual_converted"] = (
    experiments["user_id"].isin(converted_users).astype(int)
)

# Calculate metrics for each group
results = experiments.groupby("experiment_group").agg(
    total_users=("user_id", "nunique"),
    converted_users=("actual_converted", "sum")
).reset_index()

results["conversion_rate"] = (
    results["converted_users"] / results["total_users"]
)

results["conversion_rate_pct"] = (
    results["conversion_rate"] * 100
).round(2)

print("\n--- A/B TEST RESULTS ---")
print(results.to_string(index=False))

# Prepare statistical comparison
groups = results.set_index("experiment_group")

# Identify the control and treatment groups
if not {"Control", "Treatment"}.issubset(groups.index):
    raise ValueError(
        "Expected Control and Treatment groups. Check experiments.csv."
    )

a = groups.loc["Control"]
b = groups.loc["Treatment"]

rate_a = a["conversion_rate"]
rate_b = b["conversion_rate"]

# Absolute difference in percentage points
difference = (rate_b - rate_a) * 100

# Relative lift compared with Group A
relative_lift = (
    ((rate_b - rate_a) / rate_a) * 100
    if rate_a > 0 else float("nan")
)

# Two-proportion z-test using a pooled proportion
n_a = int(a["total_users"])
n_b = int(b["total_users"])
x_a = int(a["converted_users"])
x_b = int(b["converted_users"])

pooled_rate = (x_a + x_b) / (n_a + n_b)

standard_error = math.sqrt(
    pooled_rate * (1 - pooled_rate) * (1 / n_a + 1 / n_b)
)

if standard_error > 0:
    z_score = (rate_b - rate_a) / standard_error

    # Approximate two-sided p-value using the normal distribution
    p_value = math.erfc(abs(z_score) / math.sqrt(2))
else:
    z_score = 0.0
    p_value = 1.0

print("\n--- STATISTICAL COMPARISON ---")
print(f"Group A Conversion Rate: {rate_a * 100:.2f}%")
print(f"Group B Conversion Rate: {rate_b * 100:.2f}%")
print(f"Absolute Difference: {difference:.2f} percentage points")
print(f"Relative Lift: {relative_lift:.2f}%")
print(f"Z-score: {z_score:.4f}")
print(f"P-value: {p_value:.4f}")

if p_value < 0.05:
    print("Result: Statistically significant at the 5% level.")
else:
    print("Result: Not statistically significant at the 5% level.")

# Export the results
results.to_csv(
    OUTPUT_DIR / "ab_testing_results.csv",
    index=False
)

print("\nResults saved to screenshots/ab_testing_results.csv")