# Week 2 KPI Definitions Template

This template documents the calculations to be used for the Week 2 KPI analysis.

**Source dataset:** `data/processed/standardized_superstore.csv`

**Supported source fields:** `Sales`, `Profit`, `Order ID`, `Order Date`, `Quantity`, `Discount`, `Category`, `Sub-Category`, `Region`, `Segment`, `Customer ID`

## Verified dataset baseline

| Check | Verified result |
|---|---:|
| Transaction rows | 10,194 |
| Dataset columns | 21 |
| Distinct orders | 5,111 |
| Distinct customers | 804 |
| Total Sales | $2,326,534.35 |
| Total Profit | $292,296.81 |
| Profit Margin | 12.56% |
| Average Order Value | $455.20 |
| Order-date range | 3 January 2023 to 30 December 2026 |
| Missing values in Sales, Profit, Order ID, or Order Date | 0 |
| Duplicate rows | 0 |
| Negative-profit transaction rows | 1,901 |
| Total negative profit | -$157,038.93 |

The verified totals are based on the cleaned dataset. `Order ID` repeats for multiple product lines, so Order Volume must use a distinct count rather than transaction-row count.

## Annual Revenue baseline

| Year | Sales | Profit | Distinct Orders |
|---|---:|---:|---:|
| 2023 | $494,040.21 | $51,684.30 | 995 |
| 2024 | $472,993.03 | $62,020.97 | 1,053 |
| 2025 | $613,933.58 | $82,665.20 | 1,340 |
| 2026 | $745,567.53 | $95,926.35 | 1,723 |

## KPI definitions

| KPI | Business purpose | Definition / formula | Required fields | Calculation grain | Filters / exclusions | Validation method | Limitations |
|---|---|---|---|---|---|---|---|
| Total Sales | Measures total sales revenue generated during the selected period. | Sum of `Sales` | `Sales`, `Order Date` | Transaction line or selected reporting period | Include valid, non-null Sales values; use matching date filters for period comparisons | Expected baseline: $2,326,534.35. Recalculate and reconcile against the cleaned dataset | Sales values represent reported revenue; no returns or tax fields are available |
| Total Profit | Measures total profit earned during the selected period. | Sum of `Profit` | `Profit`, `Order Date` | Transaction line or selected reporting period | Include valid, non-null Profit values; retain negative profit values | Expected baseline: $292,296.81. Recalculate and reconcile against the cleaned dataset | 1,901 transactions have negative profit totaling -$157,038.93 |
| Order Volume | Counts the number of distinct customer orders. | Count of distinct valid `Order ID` values | `Order ID`, `Order Date` | One result per selected reporting period | Exclude null or blank `Order ID` values; apply period filters consistently | Expected baseline: 5,111 distinct orders | The 10,194 rows include repeated order IDs for multi-line orders |
| Average Order Value (AOV) | Measures average sales generated per eligible distinct order. | Total Sales / Count of distinct eligible `Order ID` values | `Sales`, `Order ID`, `Order Date` | One result per selected reporting period | Exclude blank order IDs and do not double-count multi-line orders | Expected baseline: $455.20 using $2,326,534.35 / 5,111 | AOV is sensitive to cancellations or returns if those fields become available |
| Profit Margin | Measures the percentage of sales retained as profit. | `(Total Profit / Total Sales) × 100` | `Sales`, `Profit`, `Order Date` | Period, category, region, segment, or other approved group | Exclude calculations where Total Sales equals zero or is null | Expected baseline: 12.56% using $292,296.81 / $2,326,534.35 | The margin is a ratio and should not be compared where the sales base is extremely small |
| Revenue Growth | Measures the percentage change in sales between two comparable periods. | `(Current Revenue - Previous Comparable Revenue) / Previous Comparable Revenue × 100` | `Sales`, `Order Date` | Comparable time periods, such as year or month | Exclude periods with no prior revenue; use equal and complete comparison periods | Recalculate using annual Sales totals; verify against the annual baseline table | Confirm that periods are comparable before presenting growth; 2026 is the latest year in the dataset |

## Calculation rules

- Use only the fields available in the analysis-ready dataset.
- Keep negative `Profit` values because they represent genuine losses.
- Count an order once using the distinct `Order ID`.
- Use transaction-line `Sales` and `Profit` values when aggregating KPI totals.
- Use consistent date ranges for comparable-period calculations.
- Round displayed percentage results appropriately, while retaining full precision for intermediate calculations.
- Apply the same filters to all KPI outputs used in a single comparison.

## Required Week 2 checks

- Confirm row count and column structure of the standardized dataset.
- Confirm that `Order ID` is unique only within an order and may repeat across product-line rows.
- Confirm no invalid or missing values exist in `Sales`, `Profit`, or `Order ID`.
- Confirm the cleaned dataset contains 10,194 transaction rows and 21 columns.
- Confirm the verified overall baseline totals and the 5,111 distinct orders.
- Reconcile Total Sales and Total Profit against independent source and processed totals.
- Confirm that the distinct order count is not based on row count.
- Document the exact date ranges used for each KPI.
- State clearly when a KPI is not defensible due to unavailable or incomplete data.

## Expected output

The final KPI documentation should be maintained in `kpi_definitions.xlsx`. This template is for planning and review before the final definitions and calculations are completed.
