
# Blinkit Delivery SLA Diagnostic — Dashboard Specification

## 1. Objective

The dashboard diagnoses delivery SLA performance across Mumbai and Bengaluru using simulated order data from 2026-10-05 to 2026-11-01.

The objective is to identify which dark-store clusters, hour bands and product categories have the lowest compliance with the 10-minute delivery promise.

The SLA rule is fixed: an order is on time when delivery_minutes <= 10. Cancelled orders are excluded from the compliance denominator.

All data in this project is simulated and does not represent actual Blinkit operations.

## 2. Data Sources

| Worksheet | Data source | Purpose |
|---|---|---|
| W1 Daily Trend | daily_compliance.csv | Daily compliance trend |
| W2 Cluster-Band Cells | cluster_band_cells.csv | Compare all cluster-hour cells |
| W3 Worst N | cluster_band_cells.csv | Display the lowest N cells |
| W4 Category | category_compliance.csv | Compare category compliance |
| W5 Big Numbers | kpi_summary.csv | Display headline KPIs |

## 3. Worksheet Specifications

### W1 — Daily Trend

**Chart type:** Line chart

**Data source:** `daily_compliance.csv`

**Columns shelf:** `order_date`

**Rows shelf:** `compliance_pct`

**Marks card:**
- Mark type: Line
- Colour: Blue
- Detail: `order_date`
- Show daily compliance values where readable.

**Filters and sorting:**
- Include all 28 dates.
- Sort `order_date` ascending.
- No city filter.

**Point annotation:**

Add a point annotation to the lowest day:

"Lowest daily compliance: 72.86% on 2026-10-31."

**Area annotation:**

Add an area annotation over the last seven days:

"Last 7 days compliance was 76.14%, compared with 80.97% in the first 7 days."

**Values displayed:**
- First day (2026-10-05): 76.50%
- Last day (2026-11-01): 73.91%
- Lowest day (2026-10-31): 72.86%
- First 7 days: 80.97%
- Last 7 days: 76.14%

### W2 — Cluster-Band Cells

**Chart type:** Horizontal bar chart

**Data source:** `cluster_band_cells.csv`

**Columns shelf:** `compliance_pct`

**Rows shelf:** `cell_label`

**Marks card:**
- Mark type: Bar
- Colour: Highlight the three lowest-compliance cells in orange/red.
- Colour all remaining cells grey.
- Show mark labels.
- Label field: `compliance_pct`.

**Filters and sorting:**
- Sort `cell_label` by `compliance_pct` ascending.
- Display all 24 cells.
- Add a `city` filter to the dashboard.
- The city filter applies to W2 only.

**Highlighted bottleneck cells:**

| Rank | Cell | Compliance |
|---:|---|---:|
| 1 | Whitefield - Lunch | 42.63% |
| 2 | Andheri - Evening | 48.49% |
| 3 | Koramangala - Evening | 59.54% |

**Purpose:** Identify the lowest-performing cluster-hour combinations.

### W3 — Worst N

**Chart type:** Horizontal bar chart

**Data source:** `cluster_band_cells.csv`

**Columns shelf:** `compliance_pct`

**Rows shelf:** `cell_label`

**Marks card:**
- Mark type: Bar
- Colour: Red/orange.
- Show compliance percentage labels.

**Parameter:**
- Name: `Worst N`
- Data type: Integer
- Current value: 3
- Minimum value: 3
- Maximum value: 7
- Step size: 1

**Filter and sorting:**
- Use a Top-and-Bottom filter to retain the bottom N cells by `compliance_pct`.
- Sort ascending.
- No city filter is applied to W3.

**Values displayed at N = 3:**

| Cell | Compliance |
|---|---:|
| Whitefield - Lunch | 42.63% |
| Andheri - Evening | 48.49% |
| Koramangala - Evening | 59.54% |

**Values displayed at N = 5:**

| Cell | Compliance |
|---|---:|
| Whitefield - Lunch | 42.63% |
| Andheri - Evening | 48.49% |
| Koramangala - Evening | 59.54% |
| Powai - Evening | 74.26% |
| Powai - Lunch | 77.87% |

**Purpose:** Allow the operations director to adjust the number of bottleneck cells being reviewed.

### W4 — Category

**Chart type:** Horizontal bar chart

**Data source:** `category_compliance.csv`

**Columns shelf:** `compliance_pct`

**Rows shelf:** `category`

**Marks card:**
- Mark type: Bar
- Highlight `Fruits & Vegetables` in orange/red.
- Colour the other four categories grey.
- Show compliance percentage labels.

**Filters and sorting:**
- Sort ascending by `compliance_pct`.
- Include all five categories.
- No city filter.

**Values displayed:**

| Category | Compliance |
|---|---:|
| Fruits & Vegetables | 62.40% |
| Household | 81.63% |
| Snacks & Beverages | 83.56% |
| Personal Care | 84.57% |
| Dairy & Bread | 84.74% |

**Purpose:** Identify the product category with the lowest SLA compliance.

### W5 — Big Numbers

**Chart type:** Three KPI text views

**Data source:** `kpi_summary.csv`

**Columns shelf:** None

**Rows shelf:** None

**Marks card:**
- Mark type: Text
- Use enlarged text.
- Display percentage values prominently.
- Give each KPI a clear descriptive title.

**Values displayed:**

| KPI | Value |
|---|---:|
| Overall compliance | 79.01% |
| First 7 days compliance | 80.97% |
| Last 7 days compliance | 76.14% |

**Purpose:** Provide a quick summary of overall performance and the change between the first and last seven days.

## 4. Dashboard Assembly and Interactivity

**Dashboard title:**

Blinkit Delivery SLA Diagnostic — Mumbai & Bengaluru

**Dashboard size:** Fixed 1200 × 768 pixels.

**Layout order:**
1. W5 Big Numbers — top row.
2. W1 Daily Trend — upper section.
3. W2 Cluster-Band Cells — central section.
4. W3 Worst N — lower section.
5. W4 Category — bottom section.

**City filter:**
- Add a `city` filter from W2.
- Apply the filter to W2 only.
- Do not apply it to W1, W3, W4 or W5.

**Reason for excluding W3:**

W3 must show the lowest N cells from the complete dataset. Applying a city filter could reduce the number of available cells and change the intended lowest-N comparison. Therefore, W3 is deliberately excluded from the city filter.

**Click-to-filter interaction:**

Configure a dashboard Filter Action:
- Source worksheet: W2 Cluster-Band Cells.
- Target worksheet: W3 Worst N.
- Run action on: Select.
- Use `cell_label` as the matching field.

When the user clicks the `Whitefield - Lunch` bar in W2, W3 should display only:

| Cell | Compliance |
|---|---:|
| Whitefield - Lunch | 42.63% |

**Worksheets not reached by the city filter:** W1, W3, W4 and W5.

## 5. Five-Point Data Story

### Point 1 — Overall SLA Performance

**Caption:** Overall delivery SLA compliance is 79.01%, below the 80% target.

**View:** W5 Big Numbers.

**Annotation:** The overall compliance benchmark is 80%.

### Point 2 — Daily Performance Trend

**Caption:** Compliance declined from 76.50% on the first day to 73.91% on the last day.

**View:** W1 Daily Trend.

**Annotation:** The lowest daily compliance was 72.86% on 2026-10-31.

### Point 3 — Bottleneck Identification

**Caption:** Whitefield - Lunch records the lowest cell compliance at 42.63%.

**View:** W2 Cluster-Band Cells.

**Annotation:** The three lowest cells are Whitefield - Lunch (42.63%), Andheri - Evening (48.49%) and Koramangala - Evening (59.54%).

### Point 4 — Focused Bottleneck Review

**Caption:** The lowest 3 cells range from 42.63% to 59.54% compliance.

**View:** W3 Worst N.

**Annotation:** Selecting Whitefield - Lunch in W2 filters W3 to that single cell at 42.63%.

### Point 5 — Category Performance

**Caption:** Fruits & Vegetables has the lowest category compliance at 62.40%.

**View:** W4 Category.

**Annotation:** The other four categories range from 81.63% to 84.74%.

## 6. Key Findings and Limitations

- Overall compliance is 79.01%, slightly below the 80% target.
- Whitefield - Lunch is the weakest cluster-hour cell at 42.63%.
- Andheri - Evening is the second weakest cell at 48.49%.
- Koramangala - Evening is the third weakest cell at 59.54%.
- Fruits & Vegetables has the lowest category compliance at 62.40%.
- Last-seven-day compliance is 76.14%, compared with 80.97% in the first seven days.

The dataset is simulated. It identifies performance patterns but does not establish the real operational causes of delays. Single-day compliance figures can be noisy because they are based on approximately 200 delivered orders per day. The dashboard is a diagnostic tool, not a real-time monitoring system.
