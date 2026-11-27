# Blinkit Delivery SLA Diagnostic

## Project Overview

The Blinkit Delivery SLA Diagnostic project focuses on analyzing delivery performance and identifying factors affecting delivery SLA compliance.

The project uses SQL, Python, SQLite, Microsoft Excel, and Tableau Public to examine delivery performance, analyze operational patterns, and generate actionable insights.

The analysis is based on a simulated dataset covering Mumbai and Bengaluru from 5 October 2026 to 1 November 2026.

## Project Objectives

- Analyze delivery SLA compliance.
- Evaluate delivery performance across different segments.
- Identify delivery time patterns and operational bottlenecks.
- Summarize key performance indicators (KPIs).
- Present findings through a Tableau dashboard.

## Tools & Technologies

- **SQL:** Data analysis, aggregations, joins, segmentation, and trend analysis.
- **Python:** Data generation and CSV exports.
- **SQLite:** Database management.
- **Microsoft Excel:** Spreadsheet analysis and KPI review.
- **Tableau Public:** Dashboard visualization.
- **GitHub:** Project version control and documentation.

## Repository Structure

```text
Blinkit-Delivery-SLA-Diagnostic/
│
├── dashboards/
│   └── tableau/
│       └── Blinkit_Delivery_SLA_Diagnostic.twbx
│
├── data/
│   ├── database/
│   │   └── blinkit_sla.db
│   │
│   ├── exports/
│   │   └── blinkit_sla_analysis.xlsx
│   │
│   └── processed/
│       ├── category_compliance.csv
│       ├── cluster_band_cells.csv
│       ├── daily_compliance.csv
│       ├── focus_delivery_minutes.csv
│       └── kpi_summary.csv
│
├── docs/
│   ├── ai_log.md
│   ├── dashboard_spec.md
│   ├── one_page_report.md
│   └── requirements.md
│
├── python/
│   ├── export_data.py
│   └── generate_data.py
│
├── sql/
│   ├── 01_foundations.sql
│   ├── 02_aggregation_joins.sql
│   ├── 03_segments.sql
│   ├── 04_trend.sql
│   └── verify.sql
│
└── README.md
```

## Key Analysis Areas

1. Delivery SLA compliance analysis.
2. Aggregation and join-based analysis.
3. Segment-level performance analysis.
4. Delivery trend analysis.
5. KPI summaries and data verification.

## Tableau Dashboard

The packaged Tableau workbook is available at:

`dashboards/tableau/Blinkit_Delivery_SLA_Diagnostic.twbx`

The dashboard presents:

- Daily SLA compliance trends.
- Cluster and time-band performance.
- Worst-performing delivery segments.
- Category-level compliance.
- Overall KPI summaries.

## Data Files

- **SQLite Database:** `data/database/blinkit_sla.db`
- **Processed CSV Files:** `data/processed/`
- **Excel Analysis Workbook:** `data/exports/blinkit_sla_analysis.xlsx`

## Documentation

Additional project documentation is available in the `docs/` directory:

- `requirements.md` – Project requirements and analytical definitions.
- `dashboard_spec.md` – Tableau dashboard specifications.
- `one_page_report.md` – Key findings and recommendations.
- `ai_log.md` – AI assistance and validation record.

## Important Note

This project uses a simulated dataset for analytical and educational purposes. It does not represent actual Blinkit operational data.

## Author

**Nashid**
GitHub: [usmaninashid98](https://github.com/usmaninashid98)