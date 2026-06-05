-- creating business metrics

-- 1. overall churn rate
SELECT
    ROUND(
        100.0 *
        SUM(CASE WHEN Churn='Yes' THEN 1 ELSE 0 END)
        / COUNT(*),
        2
    ) AS ChurnRate
FROM customers;
-- 26.58

-- 2. monthly revenue
SELECT
    SUM(MonthlyCharges) AS MonthlyRevenue
FROM customers;
-- 455661.0000000003

-- 3. revenue lost from churn
SELECT
    SUM(MonthlyCharges) AS RevenueLost
FROM customers
WHERE Churn='Yes';
-- 139130.84999999986

-- 4. average revenue per user
SELECT
    AVG(MonthlyCharges) AS ARPU
FROM customers;
-- 64.79820819112632


