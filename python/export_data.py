
import sqlite3
import csv

conn = sqlite3.connect("blinkit_sla.db")

def export_csv(filename, query):
    cursor = conn.execute(query)
    columns = [description[0] for description in cursor.description]
    rows = cursor.fetchall()

    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(columns)
        writer.writerows(rows)

    print(f"{filename} created: {len(rows)} rows")


# 1. Cluster and hour-band compliance
export_csv("cluster_band_cells.csv", """
WITH cell_summary AS (
    SELECT
        ds.city,
        ds.cluster,
        h.band,
        ds.cluster || ' - ' || h.band AS cell_label,
        COUNT(o.delivery_minutes) AS delivered_orders,
        SUM(o.within_sla) AS within_sla_orders,
        ROUND(
            SUM(o.within_sla) * 100.0 /
            COUNT(o.delivery_minutes), 2
        ) AS compliance_pct,
        ROUND(AVG(o.delivery_minutes), 2) AS avg_minutes
    FROM orders o
    JOIN dark_stores ds ON o.store_id = ds.store_id
    JOIN hour_bands h
      ON STRFTIME('%H', o.order_ts) = h.hour_text
    WHERE o.status = 'Delivered'
    GROUP BY ds.city, ds.cluster, h.band
    HAVING COUNT(o.delivery_minutes) >= 150
),
ranked AS (
    SELECT *,
        RANK() OVER (
            PARTITION BY city ORDER BY compliance_pct ASC
        ) AS rank_in_city,
        RANK() OVER (
            ORDER BY compliance_pct ASC
        ) AS rank_overall
    FROM cell_summary
)
SELECT
    city, cluster, band, cell_label,
    delivered_orders, within_sla_orders,
    compliance_pct, avg_minutes, rank_overall
FROM ranked
ORDER BY rank_overall;
""")


# 2. Daily compliance
export_csv("daily_compliance.csv", """
SELECT
    order_date,
    COUNT(delivery_minutes) AS delivered_orders,
    ROUND(
        SUM(within_sla) * 100.0 /
        COUNT(delivery_minutes), 2
    ) AS compliance_pct
FROM orders
GROUP BY order_date
ORDER BY order_date;
""")


# 3. Category compliance - all five categories
export_csv("category_compliance.csv", """
SELECT
    category,
    COUNT(delivery_minutes) AS delivered_orders,
    ROUND(
        SUM(within_sla) * 100.0 /
        COUNT(delivery_minutes), 2
    ) AS compliance_pct
FROM orders
WHERE status = 'Delivered'
GROUP BY category
ORDER BY compliance_pct ASC;
""")


# 4. KPI summary
export_csv("kpi_summary.csv", """
SELECT
    ROUND(
        SUM(within_sla) * 100.0 /
        COUNT(delivery_minutes), 2
    ) AS overall_compliance_pct,

    ROUND(
        SUM(CASE
            WHEN order_date BETWEEN '2026-10-05' AND '2026-10-11'
            THEN within_sla ELSE 0
        END) * 100.0 /
        SUM(CASE
            WHEN order_date BETWEEN '2026-10-05' AND '2026-10-11'
            THEN CASE WHEN delivery_minutes IS NOT NULL
                      THEN 1 ELSE 0 END
            ELSE 0
        END), 2
    ) AS first_7_days_pct,

    ROUND(
        SUM(CASE
            WHEN order_date BETWEEN '2026-10-26' AND '2026-11-01'
            THEN within_sla ELSE 0
        END) * 100.0 /
        SUM(CASE
            WHEN order_date BETWEEN '2026-10-26' AND '2026-11-01'
            THEN CASE WHEN delivery_minutes IS NOT NULL
                      THEN 1 ELSE 0 END
            ELSE 0
        END), 2
    ) AS last_7_days_pct
FROM orders;
""")


# 5. Delivery minutes for the three focus cells
export_csv("focus_delivery_minutes.csv", """
WITH cell_summary AS (
    SELECT
        ds.city,
        ds.cluster,
        h.band,
        ROUND(
            SUM(o.within_sla) * 100.0 /
            COUNT(o.delivery_minutes), 2
        ) AS compliance_pct
    FROM orders o
    JOIN dark_stores ds ON o.store_id = ds.store_id
    JOIN hour_bands h
      ON STRFTIME('%H', o.order_ts) = h.hour_text
    WHERE o.status = 'Delivered'
    GROUP BY ds.city, ds.cluster, h.band
    HAVING COUNT(o.delivery_minutes) >= 150
),
ranked AS (
    SELECT *,
        RANK() OVER (
            PARTITION BY city ORDER BY compliance_pct ASC
        ) AS rank_in_city,
        RANK() OVER (
            ORDER BY compliance_pct ASC
        ) AS rank_overall
    FROM cell_summary
),
chosen_cells AS (
    SELECT city, cluster, band
    FROM ranked
    WHERE rank_in_city = 1

    UNION

    SELECT city, cluster, band
    FROM ranked
    WHERE rank_overall = (
        SELECT MAX(rank_overall) FROM ranked
    )
)
SELECT
    o.order_id,
    ds.city,
    ds.cluster,
    h.band,
    o.delivery_minutes
FROM orders o
JOIN dark_stores ds ON o.store_id = ds.store_id
JOIN hour_bands h
  ON STRFTIME('%H', o.order_ts) = h.hour_text
JOIN chosen_cells c
  ON ds.city = c.city
 AND ds.cluster = c.cluster
 AND h.band = c.band
WHERE o.status = 'Delivered'
ORDER BY ds.cluster, h.band, o.order_id;
""")

conn.close()
print("All five CSV exports completed.")
