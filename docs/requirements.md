
# Blinkit Delivery SLA Diagnostic

## 1. Stakeholder Grid

| Stakeholder | Interest | Influence | Quadrant | Action |
|---|---|---|---|---|
| Regional Operations Director | Cares a lot | Can change, approve or block the work | Manage Closely | Review findings and approve operational decisions |
| Dark-Store Managers | Cares a lot | Can change, approve or block the work | Manage Closely | Share cluster-level problems and coordinate improvements |
| Rider-Fleet Lead | Cares a lot | Can change, approve or block the work | Manage Closely | Use findings to plan rider allocation |
| Finance Team | Cares less | Can change, approve or block the work | Keep Satisfied | Share cost implications of proposed changes |
| Category Team | Cares a lot | Cannot change the work | Keep Informed | Share category-level compliance findings |
| Customers | Cares a lot | Cannot change the work | Keep Informed | Consider delivery experience and customer impact |
| Data Team | Cares a lot | Can change, approve or block the work | Manage Closely | Validate delivery-time data and KPI calculations |
**Official number owners:** The Regional Operations Director owns the Sub-10-Minute Compliance KPI. The Data Team is responsible for the underlying delivery-time and order data used to calculate it.


## 2. Questions and Playback

### Rewritten Questions

**Question 1**

Original: "Do you want a bar chart or a line chart?"

Rewritten: "How do you currently identify which dark-store clusters and hours have the biggest delivery delays?"

Why the original question was poor: It focuses on chart preference instead of understanding the business problem.

**Question 2**

Original: "Should it be real-time?"

Rewritten: "How frequently do you need delivery compliance information to make staffing and rider-allocation decisions?"

Why the original question was poor: It assumes real-time information is necessary without understanding the decision frequency.

**Question 3**

Original: "Do you need every late order listed?"

Rewritten: "What information would help you identify and prioritize the clusters and hours that need operational attention?"

Why the original question was poor: It focuses on listing individual orders rather than identifying actionable patterns.

### Playback

The Regional Operations Director asked for a real-time dashboard showing every late order across all stores. After understanding her requirements, I found that she mainly needs to know which clusters and hours are missing the 10-minute delivery target. Today, she only gets one weekly city-level average, so it is difficult to identify the problem areas. She wants to use this information to decide where to add riders or staff and where to hold back new-customer promotions. Since a weekly review is enough for her, I will build a weekly report showing delivery compliance by city, cluster, hour band and category. The target is to achieve at least 80% compliance in every cluster and every hour band.


## 3. Ask → Need → Build

| What the director asked for | What she actually needs | What I will build |
|---|---|---|
| A real-time dashboard showing every late order across all stores | A clear view of which dark-store clusters and hours are missing the 10-minute target | A weekly delivery compliance view by cluster and hour band |
| One overall city-level compliance figure | To identify exactly which clusters are performing poorly instead of depending on customer complaints | A breakdown of compliance by city and individual cluster |
| Riders are being added everywhere | To know where additional riders or staff are actually needed | A ranked view of the weakest cluster and hour-band combinations |
| Information about delivery performance | To decide where new-customer promotions should be held back | A category and cluster-level compliance analysis to support operational decisions |

### Need Statement

The Regional Operations Director needs to identify underperforming dark-store clusters and hour bands every week so that she can make better rider-allocation, staffing and promotion decisions.


## 4. KPI Definition

### KPI: Sub-10-Minute Compliance

| Field | Definition |
|---|---|
| Name | Sub-10-Minute Compliance |
| Definition | The percentage of delivered orders completed within 10 minutes or less. |
| Question answered | What percentage of delivered orders meet the 10-minute delivery promise, and which clusters and hour bands are below the target? |
| Formula | (Number of delivered orders with delivery_minutes <= 10 / Total delivered orders) * 100. In SQL: SUM(within_sla) * 100.0 / COUNT(delivery_minutes). |
| Counted on | Delivered orders only. Cancelled orders are excluded because they have no delivery time. |
| Date used | order_date |
| Cut by | City, dark-store cluster, hour band and product category |
| Target | At least 80% compliance in every cluster and every hour band. |
| Deadline | By the end of the next quarter |
| Starting point | To be filled after Part B, Task 3, using the overall compliance result from SQL. |
| Owner | Regional Operations Director |
| Source | orders table in blinkit_sla.db |

### Boundary Note

The SLA boundary is fixed at delivery_minutes <= 10. An order delivered in exactly 10 minutes counts as on time. If we use delivery_minutes < 10 instead, orders taking exactly 10 minutes will be treated as late. This changes the reported compliance percentage and can affect operational decisions. Therefore, the boundary must be clearly documented and used consistently.

The overall compliance figures under both rules (<= 10 and < 10) will be added here after Part B, Task 3.

## 5. Decision Log and Scope

### Decision Log

| Date | Decision | Roles Agreed | Why It Matters |
|---|---|---|---|
| 2026-11-18 | Use delivery_minutes <= 10 as the official on-time rule. Cancelled orders will not be included in the compliance denominator. | Regional Operations Director and Data Team | This keeps the KPI consistent and prevents cancelled orders from affecting delivery performance. |
| 2026-11-18 | Use a weekly report instead of a real-time dashboard, with compliance broken down by city, cluster, hour band and category. | Regional Operations Director, Dark-Store Managers and Rider-Fleet Lead | Weekly reporting matches the review schedule and helps the team focus on the clusters and hours that need attention. |

### Out of Scope

1. **Real-time dashboard refresh:** The director has confirmed that a weekly review is sufficient for the decisions in this project. A real-time system is not needed for this exercise.

2. **Individual late-order investigation:** The main goal is to identify repeated patterns by cluster, hour band and category, rather than investigate every late order separately.

3. **Customer-level analysis:** The available simulated dataset is designed for operational SLA analysis. Customer-level behaviour and individual customer complaints are not part of this project.

4. **Actual rider performance evaluation:** The dataset does not provide individual rider-level information, so it cannot support a fair comparison of individual riders.
