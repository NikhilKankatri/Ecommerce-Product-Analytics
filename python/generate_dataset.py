from pathlib import Path

import numpy as np
import pandas as pd

# --------------------------------------------------
# 1. PROJECT SETUP
# --------------------------------------------------

PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_DIR / "data" / "raw"
DATA_DIR.mkdir(parents=True, exist_ok=True)

# Fixed seed makes the synthetic data reproducible
rng = np.random.default_rng(42)

NUM_USERS = 10_000

print("Generating ShopSphere Product Analytics datasets...")

# --------------------------------------------------
# 2. USERS DATASET
# --------------------------------------------------

user_ids = [f"U{i:05d}" for i in range(1, NUM_USERS + 1)]

signup_dates = pd.to_datetime(
    rng.integers(
        pd.Timestamp("2025-10-01").value // 10**9,
        pd.Timestamp("2026-10-01").value // 10**9,
        size=NUM_USERS
    ),
    unit="s"
).normalize()

users_df = pd.DataFrame({
    "user_id": user_ids,
    "signup_date": signup_dates,
    "country": rng.choice(
        ["India", "USA", "UK", "Canada", "Australia"],
        NUM_USERS,
        p=[0.65, 0.15, 0.08, 0.07, 0.05]
    ),
    "city": rng.choice(
        ["Bengaluru", "Mumbai", "Delhi", "Pune", "Chennai",
         "Hyderabad", "New York", "London"],
        NUM_USERS
    ),
    "device_type": rng.choice(
        ["Mobile", "Desktop", "Tablet"],
        NUM_USERS,
        p=[0.70, 0.25, 0.05]
    ),
    "acquisition_channel": rng.choice(
        ["Organic", "Paid Ads", "Social Media", "Referral", "Email"],
        NUM_USERS,
        p=[0.30, 0.25, 0.20, 0.15, 0.10]
    )
})

# --------------------------------------------------
# 3. PRODUCTS DATASET
# --------------------------------------------------

product_ids = [f"P{i:03d}" for i in range(1, 51)]

categories = [
    "Electronics", "Fashion", "Home & Kitchen",
    "Beauty", "Sports"
]

products_df = pd.DataFrame({
    "product_id": product_ids,
    "product_name": [f"Product {i:03d}" for i in range(1, 51)],
    "category": rng.choice(categories, 50),
    "price": rng.integers(199, 20000, size=50)
})

# --------------------------------------------------
# 4. EVENTS DATASET
# --------------------------------------------------

event_names = [
    "app_open",
    "view_product",
    "add_to_cart",
    "begin_checkout",
    "purchase"
]

event_rows = []
order_rows = []
experiment_rows = []

order_counter = 1
event_counter = 1

for user in users_df.itertuples(index=False):
    # Each user has a signup date and a sequence of product actions
    session_count = int(rng.integers(1, 6))

    for session_number in range(session_count):
        session_id = f"S{user.user_id[1:]}_{session_number + 1}"

        session_start = (
            user.signup_date
            + pd.Timedelta(days=int(rng.integers(0, 180)))
            + pd.Timedelta(minutes=int(rng.integers(0, 1440)))
        )

        product = products_df.iloc[int(rng.integers(0, len(products_df)))]
        product_id = product["product_id"]

        actions = ["app_open", "view_product"]

        add_to_cart = rng.random() < 0.35
        checkout = add_to_cart and rng.random() < 0.60
        purchase = checkout and rng.random() < 0.45

        if add_to_cart:
            actions.append("add_to_cart")
        if checkout:
            actions.append("begin_checkout")
        if purchase:
            actions.append("purchase")

        for action_number, event_name in enumerate(actions):
            event_time = (
                session_start
                + pd.Timedelta(minutes=action_number * 2)
            )

            event_rows.append({
                "event_id": f"E{event_counter:07d}",
                "user_id": user.user_id,
                "session_id": session_id,
                "event_name": event_name,
                "event_timestamp": event_time,
                "product_id": product_id
            })

            event_counter += 1

        # Record an order whenever a purchase event occurs
        if purchase:
            quantity = int(rng.integers(1, 4))
            total_amount = int(product["price"] * quantity)

            order_rows.append({
                "order_id": f"O{order_counter:06d}",
                "user_id": user.user_id,
                "session_id": session_id,
                "product_id": product_id,
                "order_date": session_start + pd.Timedelta(minutes=8),
                "quantity": quantity,
                "total_amount": total_amount
            })

            order_counter += 1

# --------------------------------------------------
# 5. CONVERT EVENTS AND ORDERS TO DATAFRAMES
# --------------------------------------------------

events_df = pd.DataFrame(event_rows)
orders_df = pd.DataFrame(order_rows)

# --------------------------------------------------
# 6. A/B TESTING DATASET
# --------------------------------------------------

experiment_users = rng.choice(
    user_ids,
    size=NUM_USERS,
    replace=False
)

experiment_df = pd.DataFrame({
    "experiment_id": "checkout_redesign_01",
    "user_id": experiment_users,
    "experiment_group": rng.choice(
        ["Control", "Treatment"],
        size=NUM_USERS
    ),
    "assignment_timestamp": pd.Timestamp("2026-09-01"),
    "converted": rng.choice(
        [0, 1],
        size=NUM_USERS,
        p=[0.75, 0.25]
    )
})

# --------------------------------------------------
# 7. SAVE ALL DATASETS
# --------------------------------------------------

datasets = {
    "users.csv": users_df,
    "products.csv": products_df,
    "events.csv": events_df,
    "orders.csv": orders_df,
    "experiments.csv": experiment_df
}

for filename, dataframe in datasets.items():
    output_path = DATA_DIR / filename
    dataframe.to_csv(output_path, index=False)
    print(f"Saved {filename}: {len(dataframe):,} rows")

print("\nAll datasets generated successfully!")
print(f"Location: {DATA_DIR}")