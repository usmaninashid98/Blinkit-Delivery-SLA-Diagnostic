
-- Blinkit SLA Diagnostic
-- Part B - Task 2: Data Verification

-- 1. Count rows in dark_stores
SELECT COUNT(*) AS dark_stores_count
FROM dark_stores;

-- 2. Count rows in hour_bands
SELECT COUNT(*) AS hour_bands_count
FROM hour_bands;

-- 3. Count rows in orders
SELECT COUNT(*) AS orders_count
FROM orders;

-- 4. Count orders by status
SELECT status, COUNT(*) AS order_count
FROM orders
GROUP BY status
ORDER BY status;

-- Verification results:
-- dark_stores: 13
-- hour_bands: 17
-- orders: 6000
-- Cancelled: 384
-- Delivered: 5616
