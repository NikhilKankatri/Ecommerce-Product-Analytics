# Step 19: User Retention and Cohort Analysis
# Purpose: Measure how many users return after signing up.
# Business Objective: Understand user engagement and retention trends.

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

# Define project paths
PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_DIR / "data" / "cleaned"
OUTPUT_DIR = PROJECT_DIR / "screenshots"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Load datasets
users = pd.read_csv(DATA_DIR / "users_cleaned.csv")
events = pd.read_csv(DATA_DIR / "events_cleaned.csv")

# Convert date columns
users["signup_date"] = pd.to_datetime(users["signup_date"])
events["event_timestamp"] = pd.to_datetime(events["event_timestamp"])

# Assign each user to their signup-month cohort
users["cohort_month"] = (
    users["signup_date"].dt.to_period("M")
)

# Identify each user's active months
events["activity_month"] = (
    events["event_timestamp"].dt.to_period("M")
)

user_activity = events[
    ["user_id", "activity_month"]
].drop_duplicates()

# Join activity to signup cohorts
cohort_data = user_activity.merge(
    users[["user_id", "cohort_month"]],
    on="user_id",
    how="inner"
)

# Calculate the number of months since signup
cohort_data["month_number"] = (
    (cohort_data["activity_month"].dt.year
     - cohort_data["cohort_month"].dt.year) * 12
    + cohort_data["activity_month"].dt.month
    - cohort_data["cohort_month"].dt.month
)

# Exclude activity that occurred before signup
cohort_data = cohort_data[
    cohort_data["month_number"] >= 0
]

# Count active users in each cohort and month
cohort_counts = cohort_data.groupby(
    ["cohort_month", "month_number"]
)["user_id"].nunique().unstack()

# Calculate the size of each signup cohort
cohort_sizes = users.groupby(
    "cohort_month"
)["user_id"].nunique()

# Calculate monthly retention percentages
retention = cohort_counts.div(
    cohort_sizes, axis=0
) * 100

retention = retention.round(2)

# Display cohort retention table
print("\n--- COHORT RETENTION TABLE (%) ---")
print(retention.to_string())

# Export results
retention.to_csv(
    OUTPUT_DIR / "cohort_retention.csv"
)

# Visualize retention rates
plt.figure(figsize=(12, 7))

plt.imshow(
    retention.fillna(0),
    aspect="auto",
    interpolation="nearest"
)

plt.colorbar(label="Retention Rate (%)")
plt.xticks(
    range(len(retention.columns)),
    retention.columns
)

plt.yticks(
    range(len(retention.index)),
    retention.index.astype(str)
)

plt.xlabel("Months Since Signup")
plt.ylabel("Signup Cohort")
plt.title("ShopSphere User Cohort Retention")

plt.tight_layout()

chart_path = OUTPUT_DIR / "cohort_retention_heatmap.png"
plt.savefig(chart_path, dpi=150)
plt.show()

print("\nCohort analysis completed successfully!")
print(f"Retention table saved to: {OUTPUT_DIR / 'cohort_retention.csv'}")
print(f"Heatmap saved to: {chart_path}")