
-- Blinkit SLA Diagnostic
-- Part B - Task 4: Cells, Ranking and Bottleneck Patterns

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
            COUNT(o.delivery_minutes),
            2
        ) AS compliance_pct,

        ROUND(
            AVG(o.delivery_minutes),
            2
        ) AS avg_minutes

    FROM orders AS o

    INNER JOIN dark_stores AS ds
        ON o.store_id = ds.store_id

    INNER JOIN hour_bands AS h
        ON STRFTIME('%H', o.order_ts) = h.hour_text

    WHERE o.status = 'Delivered'

    GROUP BY
        ds.city,
        ds.cluster,
        h.band

    HAVING COUNT(o.delivery_minutes) >= 150
)

SELECT
    city,
    cluster,
    band,
    cell_label,
    delivered_orders,
    within_sla_orders,
    compliance_pct,
    avg_minutes,

    RANK() OVER (
        PARTITION BY city
        ORDER BY compliance_pct ASC
    ) AS rank_in_city,

    RANK() OVER (
        ORDER BY compliance_pct ASC
    ) AS rank_overall

FROM cell_summary

ORDER BY rank_overall;
