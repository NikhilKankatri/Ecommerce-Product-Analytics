# Step 17: User Conversion Funnel Analysis
# Purpose: Analyze how users progress through the shopping journey.
# Business Objective: Identify potential customer drop-off points.

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

# Define project paths
PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = PROJECT_DIR / "data" / "cleaned" / "events_cleaned.csv"
OUTPUT_DIR = PROJECT_DIR / "screenshots"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Load cleaned event data
events = pd.read_csv(DATA_FILE)

# Define funnel stages
funnel_stages = [
    ("App Open", "app_open"),
    ("Product View", "view_product"),
    ("Add to Cart", "add_to_cart"),
    ("Begin Checkout", "begin_checkout"),
    ("Purchase", "purchase"),
]

# Calculate unique users at each stage
funnel_results = []

for stage_name, event_name in funnel_stages:
    users = events.loc[
        events["event_name"] == event_name, "user_id"
    ].nunique()

    funnel_results.append({
        "Funnel Stage": stage_name,
        "Users": users
    })

funnel = pd.DataFrame(funnel_results)

# Calculate conversion from the previous stage
funnel["Conversion from Previous (%)"] = (
    funnel["Users"].div(funnel["Users"].shift(1)).mul(100).round(2)
)

# Calculate drop-off from the previous stage
funnel["Users Lost"] = (
    funnel["Users"].shift(1) - funnel["Users"]
)

print("\n--- CONVERSION FUNNEL ---")
print(funnel.to_string(index=False))

# Visualize the funnel as a bar chart
plt.figure(figsize=(10, 6))
plt.barh(funnel["Funnel Stage"], funnel["Users"])
plt.xlabel("Number of Unique Users")
plt.title("ShopSphere User Conversion Funnel")
plt.gca().invert_yaxis()
plt.tight_layout()

# Save the chart
chart_path = OUTPUT_DIR / "python_conversion_funnel.png"
plt.savefig(chart_path, dpi=150)
plt.show()

print(f"\nChart saved to: {chart_path}")