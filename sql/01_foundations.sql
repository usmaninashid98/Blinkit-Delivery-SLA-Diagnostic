
-- Blinkit SLA Diagnostic
-- Part B - Task 2: Foundational SQL Queries

-- (a) WHERE: Stores in Mumbai
SELECT *
FROM dark_stores
WHERE city = 'Mumbai';


-- (b) DISTINCT: List of all clusters
SELECT DISTINCT cluster
FROM dark_stores
ORDER BY cluster;


-- (c) LIKE: Stores whose name starts with Powai
SELECT *
FROM dark_stores
WHERE store_name LIKE 'Powai%';


-- (d) ORDER BY + LIMIT:
-- 5 slowest orders; ties broken by order_id ascending
SELECT order_id, delivery_minutes
FROM orders
WHERE delivery_minutes IS NOT NULL
ORDER BY delivery_minutes DESC, order_id ASC
LIMIT 5;


-- (e) BETWEEN: Delivered orders taking 11 to 15 minutes inclusive
SELECT *
FROM orders
WHERE status = 'Delivered'
  AND delivery_minutes BETWEEN 11 AND 15;


-- (f) IS NULL: Orders with no delivery time
SELECT *
FROM orders
WHERE delivery_minutes IS NULL;


-- (g) Alias: Minutes over the 10-minute SLA
SELECT
    order_id,
    delivery_minutes,
    delivery_minutes - 10 AS minutes_over_sla
FROM orders
WHERE status = 'Delivered';
