/* ============================================================
   RETAIL SALES & INVENTORY MANAGEMENT — SQL ANALYSIS
   Database: retail.db (SQLite)
   Tables: stores, products, sales_transactions, inventory_weekly_snapshots
   ============================================================ */


/* ------------------------------------------------------------
   1. TOTAL REVENUE, UNITS SOLD, AND ORDER COUNT BY MONTH
   Business question: How is revenue trending across the year,
   and are there seasonal peaks (e.g., Nov/Dec)?
------------------------------------------------------------ */
SELECT
    strftime('%Y-%m', date)                       AS sales_month,
    COUNT(*)                                       AS num_transactions,
    SUM(quantity_sold)                              AS units_sold,
    ROUND(SUM(total_amount), 2)                     AS revenue
FROM sales_transactions
GROUP BY sales_month
ORDER BY sales_month;


/* ------------------------------------------------------------
   2. REVENUE AND MARGIN BY PRODUCT CATEGORY
   Business question: Which categories drive the most revenue
   and profit, not just sales volume?
------------------------------------------------------------ */
SELECT
    p.category,
    SUM(s.quantity_sold)                                        AS units_sold,
    ROUND(SUM(s.total_amount), 2)                               AS revenue,
    ROUND(SUM(s.quantity_sold * p.unit_cost), 2)                AS cost_of_goods,
    ROUND(SUM(s.total_amount) - SUM(s.quantity_sold * p.unit_cost), 2) AS gross_profit,
    ROUND(100.0 * (SUM(s.total_amount) - SUM(s.quantity_sold * p.unit_cost))
          / NULLIF(SUM(s.total_amount), 0), 1)                  AS gross_margin_pct
FROM sales_transactions s
JOIN products p ON p.product_id = s.product_id
GROUP BY p.category
ORDER BY revenue DESC;


/* ------------------------------------------------------------
   3. TOP 10 BEST-SELLING PRODUCTS BY REVENUE
------------------------------------------------------------ */
SELECT
    p.product_id,
    p.product_name,
    p.category,
    SUM(s.quantity_sold)          AS units_sold,
    ROUND(SUM(s.total_amount), 2) AS revenue
FROM sales_transactions s
JOIN products p ON p.product_id = s.product_id
GROUP BY p.product_id, p.product_name, p.category
ORDER BY revenue DESC
LIMIT 10;


/* ------------------------------------------------------------
   4. STORE PERFORMANCE RANKING
   Business question: Which stores over/under-perform, and what
   is their average transaction value (basket size)?
------------------------------------------------------------ */
SELECT
    st.store_name,
    st.region,
    st.store_type,
    COUNT(*)                                    AS num_transactions,
    ROUND(SUM(s.total_amount), 2)               AS revenue,
    ROUND(AVG(s.total_amount), 2)               AS avg_transaction_value
FROM sales_transactions s
JOIN stores st ON st.store_id = s.store_id
GROUP BY st.store_name, st.region, st.store_type
ORDER BY revenue DESC;


/* ------------------------------------------------------------
   5. ABC ANALYSIS (Pareto / 80-20 inventory classification)
   Business question: Which products are "A" items (top ~80% of
   revenue) that deserve tighter inventory control?
------------------------------------------------------------ */
WITH product_revenue AS (
    SELECT
        p.product_id,
        p.product_name,
        SUM(s.total_amount) AS revenue
    FROM sales_transactions s
    JOIN products p ON p.product_id = s.product_id
    GROUP BY p.product_id, p.product_name
),
ranked AS (
    SELECT
        product_id,
        product_name,
        revenue,
        SUM(revenue) OVER (ORDER BY revenue DESC) AS running_total,
        SUM(revenue) OVER ()                       AS grand_total
    FROM product_revenue
)
SELECT
    product_id,
    product_name,
    ROUND(revenue, 2)                                          AS revenue,
    ROUND(100.0 * running_total / grand_total, 1)              AS cumulative_pct,
    CASE
        WHEN running_total / grand_total <= 0.80 THEN 'A'
        WHEN running_total / grand_total <= 0.95 THEN 'B'
        ELSE 'C'
    END                                                          AS abc_class
FROM ranked
ORDER BY revenue DESC;


/* ------------------------------------------------------------
   6. STOCKOUT FREQUENCY BY PRODUCT (weekly snapshots)
   Business question: Which products run out of stock most often,
   risking lost sales?
------------------------------------------------------------ */
SELECT
    p.product_id,
    p.product_name,
    COUNT(*)                                                   AS weeks_tracked,
    SUM(CASE WHEN i.stockout_today = 1 THEN 1 ELSE 0 END)      AS weeks_with_stockout,
    ROUND(100.0 * SUM(CASE WHEN i.stockout_today = 1 THEN 1 ELSE 0 END)
          / COUNT(*), 1)                                        AS stockout_rate_pct
FROM inventory_weekly_snapshots i
JOIN products p ON p.product_id = i.product_id
GROUP BY p.product_id, p.product_name
HAVING weeks_with_stockout > 0
ORDER BY stockout_rate_pct DESC
LIMIT 15;


/* ------------------------------------------------------------
   7. CURRENT INVENTORY POSITION vs REORDER POINT (latest snapshot)
   Business question: Which store-product combinations are AT or
   BELOW reorder point right now and need a purchase order?
------------------------------------------------------------ */
WITH latest_date AS (
    SELECT MAX(date) AS d FROM inventory_weekly_snapshots
)
SELECT
    i.store_id,
    p.product_name,
    i.stock_on_hand,
    i.reorder_point,
    (i.stock_on_hand - i.reorder_point) AS units_above_reorder_point
FROM inventory_weekly_snapshots i
JOIN products p ON p.product_id = i.product_id
JOIN latest_date ld ON i.date = ld.d
WHERE i.stock_on_hand <= i.reorder_point
ORDER BY units_above_reorder_point ASC;


/* ------------------------------------------------------------
   8. MONTH-OVER-MONTH REVENUE GROWTH (%)
   Business question: What's the MoM growth rate, and which
   months saw the sharpest swings?
------------------------------------------------------------ */
WITH monthly AS (
    SELECT
        strftime('%Y-%m', date) AS sales_month,
        SUM(total_amount)        AS revenue
    FROM sales_transactions
    GROUP BY sales_month
)
SELECT
    sales_month,
    ROUND(revenue, 2) AS revenue,
    ROUND(100.0 * (revenue - LAG(revenue) OVER (ORDER BY sales_month))
          / NULLIF(LAG(revenue) OVER (ORDER BY sales_month), 0), 1) AS mom_growth_pct
FROM monthly
ORDER BY sales_month;


/* ------------------------------------------------------------
   9. DISCOUNT / PROMOTION IMPACT
   Business question: Do discounted transactions actually sell
   more units on average than full-price ones?
------------------------------------------------------------ */
SELECT
    CASE WHEN discount_pct = 0 THEN 'Full Price' ELSE 'Discounted' END AS price_type,
    COUNT(*)                            AS num_transactions,
    ROUND(AVG(quantity_sold), 2)        AS avg_units_per_transaction,
    ROUND(SUM(total_amount), 2)         AS total_revenue
FROM sales_transactions
GROUP BY price_type;


/* ------------------------------------------------------------
   10. WEEKDAY VS WEEKEND SALES PATTERN
   Business question: Does the Fri/Sat/Sun boost built into demand
   actually show up in the data, and by how much?
------------------------------------------------------------ */
SELECT
    CASE WHEN CAST(strftime('%w', date) AS INTEGER) IN (5, 6, 0)
         THEN 'Weekend (Fri-Sun)' ELSE 'Weekday (Mon-Thu)' END AS day_type,
    COUNT(*)                        AS num_transactions,
    ROUND(SUM(total_amount), 2)     AS revenue,
    ROUND(AVG(total_amount), 2)     AS avg_transaction_value
FROM sales_transactions
GROUP BY day_type;
