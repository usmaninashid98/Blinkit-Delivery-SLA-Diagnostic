-- Blinkit SLA Diagnostic
-- Part B - Task 5: Daily and Weekly Trend

-- (a) Daily compliance for all 28 days
SELECT
    SUBSTR(order_ts, 1, 10) AS order_date,
    COUNT(delivery_minutes) AS delivered_orders,
    ROUND(
        SUM(within_sla) * 100.0 / COUNT(delivery_minutes),
        2
    ) AS compliance_pct
FROM orders
GROUP BY SUBSTR(order_ts, 1, 10)
ORDER BY order_date;


-- (b1) Compliance for the first 7 days
SELECT
    'First 7 days' AS period,
    ROUND(
        SUM(within_sla) * 100.0 / COUNT(delivery_minutes),
        2
    ) AS compliance_pct
FROM orders
WHERE SUBSTR(order_ts, 1, 10)
BETWEEN '2026-10-05' AND '2026-10-11';


-- (b2) Compliance for the last 7 days
SELECT
    'Last 7 days' AS period,
    ROUND(
        SUM(within_sla) * 100.0 / COUNT(delivery_minutes),
        2
    ) AS compliance_pct
FROM orders
WHERE SUBSTR(order_ts, 1, 10)
BETWEEN '2026-10-26' AND '2026-11-01';