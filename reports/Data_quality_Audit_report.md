# Data Quality Report

- Source file: `ecommerce-logistics-analysis\data\raw\DataCoSupplyChainDataset.csv`
- Rows: 180519
- Columns: 53
- Duplicate rows: 0
- Missing values: 336209
- Columns with missing values: 4
- High-risk columns (>10% missing): 2

## Key findings

1. The raw dataset contains no duplicate records.
2. Most columns are complete, but two fields are heavily missing: `Product Description` and `Order Zipcode`.
3. The field dictionary indicates that the dataset is a supply-chain order dataset with transactional, customer, and logistics metadata.

## Missing value summary

| Column | Dtype | Missing | Missing % | Unique |
| --- | --- | --- | --- | --- |
| Product Description | float64 | 180519 | 100.0 | 0 |
| Order Zipcode | float64 | 155679 | 86.24 | 609 |
| Customer Lname | object | 8 | 0.0 | 1109 |
| Customer Zipcode | float64 | 3 | 0.0 | 995 |
| Type | object | 0 | 0.0 | 4 |
| Days for shipping (real) | int64 | 0 | 0.0 | 7 |
| Days for shipment (scheduled) | int64 | 0 | 0.0 | 4 |
| Benefit per order | float64 | 0 | 0.0 | 21998 |
| Sales per customer | float64 | 0 | 0.0 | 2927 |
| Delivery Status | object | 0 | 0.0 | 4 |
| Late_delivery_risk | int64 | 0 | 0.0 | 2 |
| Category Id | int64 | 0 | 0.0 | 51 |

## High-risk columns

- `Product Description`
- `Order Zipcode`

## Field dictionary preview

| Field | Description |
| --- | --- |
| Type | :  Type of transaction made |
| Days for shipping (real)      | :  Actual shipping days of the purchased product |
| Days for shipment (scheduled) | :  Days of scheduled delivery of the purchased product |
| Benefit per order | :  Earnings per order placed |
| Sales per customer | :  Total sales per customer made per customer |
| Delivery Status | :  Delivery status of orders: Advance shipping , Late delivery , Shipping canceled , Shipping on time |
| Late_delivery_risk            | :  Categorical variable that indicates if sending is late (1), it is not late (0). |
| Category Id | :  Product category code |
| Category Name | :  Description of the product category |
| Customer City | :  City where the customer made the purchase |

| for more:-`DescriptionDataCoSupplyChain.csv` in data/raw/DescriptionDataCoSupplyChain.csv