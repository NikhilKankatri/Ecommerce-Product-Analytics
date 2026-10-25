-- A/B Testing Analysis
-- Purpose: Compare conversion rates between the control and variant groups.
-- Group A: Existing checkout experience.
-- Group B: Redesigned checkout experience.
-- Business Objective: Compare conversion rates across both groups.

SELECT
    experiment_group,
    COUNT(DISTINCT user_id) AS total_users,
    COUNT(DISTINCT CASE
        WHEN converted = 1 THEN user_id
    END) AS converted_users,
    ROUND(
        COUNT(DISTINCT CASE
            WHEN converted = 1 THEN user_id
        END) * 100.0
        / NULLIF(COUNT(DISTINCT user_id), 0),
        2
    ) AS conversion_rate_pct
FROM experiments
GROUP BY experiment_group
ORDER BY experiment_group;






-- Compare A/B Testing Results
-- Purpose: Compare conversion rates between the control and variant groups.
-- Uses a Common Table Expression (CTE) to calculate experiment metrics.
-- Calculates total users, converted users, and conversion rates for each group.
-- Measures the conversion rate difference in percentage points (Group B - Group A).
-- Positive difference indicates a higher conversion rate in Group B.
-- Negative difference indicates a lower conversion rate in Group B.
-- Business Objective: Evaluate whether the redesigned checkout shows potential
-- for improving user conversions.
-- Note: Statistical significance and experiment data validity must be checked
-- before making a final product decision.

-- Step 14: Compare A/B Testing Results
-- Purpose: Calculate the conversion rate difference between Group A and Group B.
-- Group A: Control group using the existing checkout.
-- Group B: Variant group using the redesigned checkout.
-- Business Objective: Measure the potential improvement from the redesign.

WITH experiment_results AS (
    SELECT
        experiment_group,
        COUNT(DISTINCT user_id) AS total_users,
        COUNT(DISTINCT CASE
            WHEN converted = 1 THEN user_id
        END) AS converted_users,
        COUNT(DISTINCT CASE
            WHEN converted = 1 THEN user_id
        END) * 100.0
            / NULLIF(COUNT(DISTINCT user_id), 0) AS conversion_rate
    FROM experiments
    GROUP BY experiment_group
)

SELECT
    experiment_group,
    total_users,
    converted_users,
    ROUND(conversion_rate, 2) AS conversion_rate_pct,
    ROUND(
        MAX(CASE WHEN experiment_group = 'B'
                 THEN conversion_rate END) OVER ()
        -
        MAX(CASE WHEN experiment_group = 'A'
                 THEN conversion_rate END) OVER (),
        2
    ) AS conversion_rate_difference_pct_points
FROM experiment_results
ORDER BY experiment_group;