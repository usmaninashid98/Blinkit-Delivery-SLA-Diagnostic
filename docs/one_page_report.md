
# Blinkit Delivery SLA Diagnostic — One-Page Report

## Executive Summary

This project analyses 6,000 simulated Blinkit orders across Mumbai and Bengaluru from 2026-10-05 to 2026-11-01. The objective is to identify where delivery performance falls short of the 10-minute SLA.

Overall SLA compliance is 79.01%, slightly below the 80% target. Cancelled orders are excluded from the delivered-order compliance denominator.

## Key Findings

1. **Overall performance:** Compliance is 79.01%, indicating that approximately 21% of delivered orders exceed the 10-minute SLA.

2. **Cluster-hour bottlenecks:** Whitefield - Lunch has the lowest compliance at 42.63%, followed by Andheri - Evening at 48.49% and Koramangala - Evening at 59.54%.

3. **Category performance:** Fruits & Vegetables has the lowest category compliance at 62.40%. The other four categories range from 81.63% to 84.74%.

4. **Daily trend:** Compliance was 80.97% during the first seven days and 76.14% during the last seven days. The lowest daily value was 72.86% on 2026-10-31.

## Recommendations

- **Investigate** Whitefield during lunch to identify operational bottlenecks.
- **Review** Andheri and Koramangala evening operations, focusing on staffing and order-handling processes.
- **Audit** the Fruits & Vegetables fulfilment process to identify possible sources of delay.
- **Monitor** daily SLA compliance and compare performance across clusters and time bands.

## Limitations

The dataset is simulated and does not represent actual Blinkit operational records. The analysis identifies where delays are concentrated but cannot establish their actual causes because detailed operational variables are unavailable.

Daily compliance figures may fluctuate because each day contains a limited number of delivered orders. Further investigation using real operational data is required before implementing major changes.
