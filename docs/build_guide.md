# Build Guide

## 1. Source data

`data/raw/data.csv` — the UCI **Online Retail** dataset: 541,909 transaction lines from a UK-based online gift retailer, 1 Dec 2010 – 9 Dec 2011.

| Column | Description |
|---|---|
| InvoiceNo | Invoice number; a leading `C` marks a cancellation |
| StockCode | Product code |
| Description | Product name |
| Quantity | Units per line (negative for returns) |
| InvoiceDate | Date and time of the invoice |
| UnitPrice | Price per unit (GBP) |
| CustomerID | Customer ID (blank for guest orders) |
| Country | Customer's country |

## 2. Data cleaning

| Issue in raw data | Rows | Action |
|---|---|---|
| Returns and cancelled invoices (`Quantity ≤ 0`) | 10,624 | Removed |
| Zero-price lines (free items, rows without a description) | 1,179 | Removed |
| Missing `CustomerID` | 132,222 after cleaning | Kept — they are real sales; excluded automatically from the customer count |

Result: **530,106 rows** → `data/clean/ecommerce_clean.xlsx`.
`scripts/clean_data.py` reproduces the same output and prints the headline figures.

## 3. Model and measures

A single table (`data`) is loaded into Power BI. Measures are in [`dax/measures.dax`](../dax/measures.dax):

- **Total Revenue** — `SUMX(data, data[Quantity] * data[UnitPrice])`
- **Total Customers** — `DISTINCTCOUNT(data[CustomerID])`
- **Total Orders** — `DISTINCTCOUNT(data[InvoiceNo])`

## 4. Report (1280 × 720, one page)

| Visual | Type | Fields |
|---|---|---|
| KPI cards | Card | Total Revenue · Total Customers · Total Orders |
| Total Revenue by Month | Line | InvoiceDate (Month) · Total Revenue |
| Total Revenue by Description | Clustered bar (scrollable) | Description · Total Revenue |
| Total Revenue by Country | Clustered column (Top 5) | Country · Total Revenue |
| Country | List slicer | Country — filters every visual |

## 5. Validation

| Check | Value |
|---|---|
| Rows after cleaning | 530,106 |
| Total Revenue | 10,644,560.42 |
| Total Customers | 4,338 |
| Total Orders | 19,962 |
| Countries / Products | 38 / 3,922 |
| United Kingdom share of revenue | 84.6% |

## Known limitations

- The month axis groups by month name, so **December** combines Dec 2010 and 1–9 Dec 2011.
- Two "Adjust bad debt" rows (invoices `A563186`, `A563187`, −11,062.06 each) remain in the cleaned data and reduce revenue by about 22K. Filtering `UnitPrice > 0` instead of `<> 0` would remove them.
- "DOTCOM POSTAGE" and "Manual" are service/adjustment lines, not products; excluding them would give a cleaner product ranking.
