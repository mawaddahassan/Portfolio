-- segment analysis

-- 1. churn by contract
SELECT
    Contract,
    COUNT(*) Customers,
    SUM(CASE WHEN Churn='Yes' THEN 1 ELSE 0 END) Churned,
    ROUND(
        100.0 *
        SUM(CASE WHEN Churn='Yes' THEN 1 ELSE 0 END)
        / COUNT(*),
        2
    ) AS ChurnRate
FROM customers
GROUP BY Contract
ORDER BY ChurnRate DESC;

-- 2. churn by internet service
SELECT
    InternetService,
    COUNT(*) Customers,
    SUM(CASE WHEN Churn='Yes' THEN 1 ELSE 0 END) Churned
FROM customers
GROUP BY InternetService;

-- 3. churn by payment method
SELECT
    PaymentMethod,
    COUNT(*) Customers,
    SUM(CASE WHEN Churn='Yes' THEN 1 ELSE 0 END) Churned
FROM customers
GROUP BY PaymentMethod;

