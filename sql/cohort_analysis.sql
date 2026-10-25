-- Step 11: Cohort Retention Analysis
-- Purpose: Measure whether users return after their signup month.
-- Cohort: Users grouped by the month they signed up.
-- Retention: Percentage of users active in a later month.

WITH user_cohorts AS (
    SELECT
        user_id,
        DATE_TRUNC('month', signup_date)::date AS cohort_month
    FROM users
),

user_activity AS (
    SELECT DISTINCT
        user_id,
        DATE_TRUNC('month', event_timestamp)::date AS activity_month
    FROM events
),

cohort_activity AS (
    SELECT
        uc.cohort_month,
        ua.activity_month,
        (
            EXTRACT(YEAR FROM AGE(ua.activity_month, uc.cohort_month)) * 12
            + EXTRACT(MONTH FROM AGE(ua.activity_month, uc.cohort_month))
        )::integer AS month_number,
        uc.user_id
    FROM user_cohorts uc
    JOIN user_activity ua
        ON uc.user_id = ua.user_id
    WHERE ua.activity_month >= uc.cohort_month
)

SELECT
    cohort_month,
    month_number,
    COUNT(DISTINCT user_id) AS active_users
FROM cohort_activity
GROUP BY cohort_month, month_number
ORDER BY cohort_month, month_number;






--Calculate Monthly Cohort Retention Rate
-- Purpose: Measure the percentage of users who remain active after signup.
-- Uses CTEs to organize user cohorts, monthly activity, and cohort sizes.
-- Calculates active users for each cohort and month.
-- Retention Rate = (Active Users / Total Cohort Users) * 100.
-- Business Objective: Understand user engagement and measure how well the
-- product retains users over time.

-- Step 12: Calculate Monthly Cohort Retention Rate
-- Purpose: Measure the percentage of users who remain active after signup.
-- Business objective: Understand user engagement and retention over time.

WITH user_cohorts AS (
    SELECT
        user_id,
        DATE_TRUNC('month', signup_date)::date AS cohort_month
    FROM users
),

user_activity AS (
    SELECT DISTINCT
        user_id,
        DATE_TRUNC('month', event_timestamp)::date AS activity_month
    FROM events
),

cohort_activity AS (
    SELECT
        uc.cohort_month,
        ua.activity_month,
        (
            EXTRACT(YEAR FROM AGE(ua.activity_month, uc.cohort_month)) * 12
            + EXTRACT(MONTH FROM AGE(ua.activity_month, uc.cohort_month))
        )::integer AS month_number,
        uc.user_id
    FROM user_cohorts uc
    JOIN user_activity ua
        ON uc.user_id = ua.user_id
    WHERE ua.activity_month >= uc.cohort_month
),

cohort_sizes AS (
    SELECT
        cohort_month,
        COUNT(DISTINCT user_id) AS cohort_users
    FROM user_cohorts
    GROUP BY cohort_month
),

monthly_retention AS (
    SELECT
        cohort_month,
        month_number,
        COUNT(DISTINCT user_id) AS active_users
    FROM cohort_activity
    GROUP BY cohort_month, month_number
)

SELECT
    mr.cohort_month,
    mr.month_number,
    cs.cohort_users,
    mr.active_users,
    ROUND(
        mr.active_users * 100.0 / NULLIF(cs.cohort_users, 0),
        2
    ) AS retention_rate_pct
FROM monthly_retention mr
JOIN cohort_sizes cs
    ON mr.cohort_month = cs.cohort_month
ORDER BY mr.cohort_month, mr.month_number;