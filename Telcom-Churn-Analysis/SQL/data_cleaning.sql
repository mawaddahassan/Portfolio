-- Data Cleaning

-- Checking nulls
SELECT *
FROM customers
WHERE TotalCharges IS NULL;

-- zero rows returned

-- check churn ditributions
SELECT Churn,
       COUNT(*) AS Customers
FROM customers
GROUP BY Churn;