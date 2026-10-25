--Conversion Funnel Analysis
-- Purpose: Count the unique users who reached each stage of the product funnel.
-- Funnel stages: App Open → Product View → Add to Cart → Begin Checkout → Purchase.
-- Business objective: Understand how users move through the shopping journey.

WITH funnel AS (
    SELECT
        COUNT(DISTINCT CASE
            WHEN event_name = 'app_open' THEN user_id
        END) AS app_open_users,

        COUNT(DISTINCT CASE
            WHEN event_name = 'view_product' THEN user_id
        END) AS product_view_users,

        COUNT(DISTINCT CASE
            WHEN event_name = 'add_to_cart' THEN user_id
        END) AS add_to_cart_users,

        COUNT(DISTINCT CASE
            WHEN event_name = 'begin_checkout' THEN user_id
        END) AS checkout_users,

        COUNT(DISTINCT CASE
            WHEN event_name = 'purchase' THEN user_id
        END) AS purchase_users

    FROM events
)

SELECT
    'App Open' AS funnel_stage,
    app_open_users AS users
FROM funnel

UNION ALL

SELECT
    'Product View',
    product_view_users
FROM funnel

UNION ALL

SELECT
    'Add to Cart',
    add_to_cart_users
FROM funnel

UNION ALL

SELECT
    'Begin Checkout',
    checkout_users
FROM funnel

UNION ALL

SELECT
    'Purchase',
    purchase_users
FROM funnel;






-- Purpose: Calculate the percentage of users progressing between funnel stages.
-- Uses the LAG() window function to compare each stage with the previous stage.
-- Business objective: Identify potential drop-off points in the customer journey.
-- Note: This query compares unique users at each stage; it does not verify that
-- users completed the stages in chronological order within the same session.

WITH funnel AS (
    SELECT
        COUNT(DISTINCT CASE
            WHEN event_name = 'app_open' THEN user_id
        END) AS app_open_users,

        COUNT(DISTINCT CASE
            WHEN event_name = 'view_product' THEN user_id
        END) AS product_view_users,

        COUNT(DISTINCT CASE
            WHEN event_name = 'add_to_cart' THEN user_id
        END) AS add_to_cart_users,

        COUNT(DISTINCT CASE
            WHEN event_name = 'begin_checkout' THEN user_id
        END) AS checkout_users,

        COUNT(DISTINCT CASE
            WHEN event_name = 'purchase' THEN user_id
        END) AS purchase_users

    FROM events
),

stages AS (
    SELECT 1 AS stage_order, 'App Open' AS stage,
           app_open_users AS users FROM funnel

    UNION ALL

    SELECT 2, 'Product View',
           product_view_users FROM funnel

    UNION ALL

    SELECT 3, 'Add to Cart',
           add_to_cart_users FROM funnel

    UNION ALL

    SELECT 4, 'Begin Checkout',
           checkout_users FROM funnel

    UNION ALL

    SELECT 5, 'Purchase',
           purchase_users FROM funnel
)

SELECT
    stage,
    users,

    ROUND(
        users * 100.0 /
        NULLIF(LAG(users) OVER (ORDER BY stage_order), 0),
        2
    ) AS conversion_from_previous_stage_pct

FROM stages
ORDER BY stage_order;