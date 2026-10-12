"""Reproduce the cleaning step: raw Online Retail CSV -> cleaned table.

Rules
  1. Keep rows with Quantity > 0   (drops returns / cancelled invoices "C...")
  2. Keep rows with UnitPrice <> 0 (drops free items and rows with no description)

Usage:  pip install pandas openpyxl
        python scripts/clean_data.py
"""
import pandas as pd

raw = pd.read_csv("data/raw/data.csv", encoding="latin1",
                  dtype={"InvoiceNo": str, "StockCode": str})
clean = raw[(raw["Quantity"] > 0) & (raw["UnitPrice"] != 0)].copy()
clean["InvoiceDate"] = pd.to_datetime(clean["InvoiceDate"])
clean["Revenue"] = clean["Quantity"] * clean["UnitPrice"]

print(f"Raw rows:        {len(raw):,}")
print(f"Clean rows:      {len(clean):,}")
print(f"Total revenue:   {clean['Revenue'].sum():,.2f}")
print(f"Customers:       {clean['CustomerID'].nunique():,}")
print(f"Orders:          {clean['InvoiceNo'].nunique():,}")
