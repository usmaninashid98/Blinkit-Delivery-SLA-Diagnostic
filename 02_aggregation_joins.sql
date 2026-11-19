
-- Blinkit SLA Diagnostic
-- Part B - Task 3: Compliance by Dimension

-- (a1) Overall compliance using <= 10 minutes
SELECT
    ROUND(SUM(within_sla) * 100.0 / COUNT(delivery_minutes), 2)
        AS overall_compliance_pct
FROM orders;


-- (a2) Overall compliance using strict < 10 minutes
SELECT
    ROUND(
        COUNT(*) * 100.0 /
        (SELECT COUNT(delivery_minutes) FROM orders),
        2
    ) AS strict_under_10_pct
FROM orders
WHERE delivery_minutes < 10;


-- (b1) Compliance by city
SELECT
    ds.city,
    ROUND(
        SUM(o.within_sla) * 100.0 / COUNT(o.delivery_minutes),
        2
    ) AS compliance_pct
FROM orders AS o
INNER JOIN dark_stores AS ds
    ON o.store_id = ds.store_id
GROUP BY ds.city
ORDER BY compliance_pct DESC;


-- (b2) Compliance by cluster
SELECT
    ds.cluster,
    ROUND(
        SUM(o.within_sla) * 100.0 / COUNT(o.delivery_minutes),
        2
    ) AS compliance_pct
FROM orders AS o
INNER JOIN dark_stores AS ds
    ON o.store_id = ds.store_id
GROUP BY ds.cluster
ORDER BY compliance_pct DESC;


-- (c) Compliance by hour band
SELECT
    h.band,
    ROUND(
        SUM(o.within_sla) * 100.0 / COUNT(o.delivery_minutes),
        2
    ) AS compliance_pct
FROM orders AS o
INNER JOIN hour_bands AS h
    ON STRFTIME('%H', o.order_ts) = h.hour_text
GROUP BY h.band
ORDER BY compliance_pct DESC;


-- (d) Compliance by category
-- Keep categories with more than 1000 delivered orders
SELECT
    o.category,
    COUNT(o.delivery_minutes) AS delivered_orders,
    ROUND(
        SUM(o.within_sla) * 100.0 / COUNT(o.delivery_minutes),
        2
    ) AS compliance_pct
FROM orders AS o
WHERE o.status = 'Delivered'
GROUP BY o.category
HAVING COUNT(o.delivery_minutes) > 1000
ORDER BY compliance_pct ASC;


-- (e) Number of orders handled by each store
-- LEFT JOIN keeps stores even when they have zero orders
SELECT
    ds.store_name,
    COUNT(o.order_id) AS orders_handled
FROM dark_stores AS ds
LEFT JOIN orders AS o
    ON ds.store_id = o.store_id
GROUP BY ds.store_id, ds.store_name
ORDER BY orders_handled ASC, ds.store_name ASC;
