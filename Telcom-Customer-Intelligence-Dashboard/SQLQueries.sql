-- Which payment methods are associated with higher customer churn?
SELECT Payment_Method
, COUNT(*)
FROM Customers
WHERE Churn_Label="Yes"
GROUP BY Payment_Method;

-- Which internet service generates the highest customer revenue?
SELECT Internet_Service,
AVG(Monthly_Charges) AS AvgRevenue
FROM Customers
GROUP BY Internet_Service;

-- Which customer segments are most likely to leave the company?
SELECT Contract
, Internet_Service,
 COUNT(*) AS TotalCustomers
FROM Customers
WHERE Customer_Status="Churrned"
GROUP BY Contract, Internet_Service;

-- Churn Rate by Contract Type 
SELECT
Contract,
COUNT(*) AS TotalCustomers,
SUM(CASE WHEN Churn='Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS ChurnRate
FROM telco_customers
GROUP BY Contract;

