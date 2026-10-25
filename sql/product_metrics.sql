----What percentage of users who viewed products eventually made a purchase?

SELECT
    COUNT(DISTINCT CASE
        WHEN event_name = 'view_product' THEN user_id
    END) AS product_viewers,

    COUNT(DISTINCT CASE
        WHEN event_name = 'purchase' THEN user_id
    END) AS purchasers,

    ROUND(
        COUNT(DISTINCT CASE
            WHEN event_name = 'purchase' THEN user_id
        END) * 100.0
        /
        NULLIF(
            COUNT(DISTINCT CASE
                WHEN event_name = 'view_product' THEN user_id
            END),
            0
        ),
        2
    ) AS conversion_rate
FROM events;





-----How many sessions added products to their carts but didn't complete a purchase?

WITH session_activity AS (
    SELECT
        session_id,
        MAX(CASE WHEN event_name = 'add_to_cart' THEN 1 ELSE 0 END) AS added_to_cart,
        MAX(CASE WHEN event_name = 'purchase' THEN 1 ELSE 0 END) AS purchased
    FROM events
    GROUP BY session_id
)

SELECT
    COUNT(*) FILTER (WHERE added_to_cart = 1) AS cart_sessions,

    COUNT(*) FILTER (
        WHERE added_to_cart = 1 AND purchased = 0
    ) AS abandoned_sessions,

    ROUND(
        100.0 * COUNT(*) FILTER (
            WHERE added_to_cart = 1 AND purchased = 0
        )
        / NULLIF(
            COUNT(*) FILTER (WHERE added_to_cart = 1), 0
        ),
        2
    ) AS cart_abandonment_rate

FROM session_activity;






------How many unique users were active each day?

SELECT
    DATE(event_timestamp) AS activity_date,
    COUNT(DISTINCT user_id) AS dau
FROM events
GROUP BY DATE(event_timestamp)
ORDER BY activity_date;






-------How many unique users were active each month?

SELECT
    DATE_TRUNC('month', event_timestamp)::DATE AS activity_month,
    COUNT(DISTINCT user_id) AS mau
FROM events
GROUP BY DATE_TRUNC('month', event_timestamp)
ORDER BY activity_month;






-------Which marketing channels generate the highest revenue?

SELECT
    u.acquisition_channel,

    COUNT(DISTINCT o.order_id) AS total_orders,

    ROUND(
        SUM(o.total_amount),
        2
    ) AS total_revenue,

    ROUND(
        AVG(o.total_amount),
        2
    ) AS average_order_value

FROM orders o

JOIN users u
    ON o.user_id = u.user_id

GROUP BY u.acquisition_channel

ORDER BY total_revenue DESC;