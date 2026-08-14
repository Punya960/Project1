# Project 1: Data Cleaning & Preparation

## Goal
Clean a raw orders dataset by handling missing values, duplicates, and
inconsistent data formats (dates, numbers, text) using Python (pandas).

## Files
- `Dataset_for_Data_Analytics.pdf` — original source file (order data)
- `raw_orders_data.csv` — data extracted from the PDF, before cleaning
- `clean_orders_data.csv` — cleaned output
- `clean.py` — extraction + cleaning script

## Source Data Challenge
The dataset was provided as a **PDF**, not a CSV/Excel file. Extracting the
text revealed that the source data itself has two built-in defects (not
caused by extraction):

1. Every `Date` value is missing its final digit
   (e.g. `2023-01-0` instead of a complete date like `2023-01-06`)
2. `"Credit Card"` is consistently truncated to `"Credit Car"` and fused
   directly onto the next field with no space
   (e.g. `Credit CarCancelled`)

Because the categories in this dataset are limited (5 products, 5 order
statuses, 5 payment methods, etc.), I used regex pattern-matching against
known vocabularies to correctly split each row instead of relying on
column position — a naive split would have corrupted the data further.

## Issues Found
- **Missing/incomplete dates:** all 1,200 rows — final digit unrecoverable
- **Truncated payment method:** "Credit Card" → "Credit Car" (fused to next field)
- **Blank coupon codes:** some orders have no coupon applied

## Cleaning Steps
1. **Parsed raw text** from the PDF using `pdftotext -layout`, then matched
   each row with a regex built from the known field vocabularies
2. **Fixed truncated text** — restored "Credit Car" to "Credit Card"
3. **Converted numeric fields** — Quantity, UnitPrice, ItemsInCart,
   TotalPrice parsed with `pd.to_numeric(errors="coerce")`
4. **Handled missing dates** — since the final digit is missing from every
   date in the source file, the day cannot be reliably reconstructed. The
   truncated value was kept in a separate `Date_Incomplete` column for
   reference, and `Date` was set to missing (`NaT`) rather than guessing
5. **Missing values** — blank coupon codes replaced with `"NoCoupon"`
6. **Verification** — checked for duplicate rows (none found) and verified
   `Quantity × UnitPrice = TotalPrice` for all rows (no mismatches)

## Result
- Rows parsed: 1,200
- Duplicate rows: 0
- Rows with unrecoverable dates: 1,200 (flagged, not guessed)

```python
import re
import pandas as pd

with open("sample.txt") as f:
    text = f.read()

row_pattern = re.compile(
    r'(ORD\d+)\s*(\d{4}-\d{2}-\d)(C\d+)\s+'
    r'(Monitor|Phone|Tablet|Chair|Printer|Desk|Laptop)\s+'
    r'(\d+)\s+([\d.]+)\s+'
    r'(\d+)\s+Main\s+'
    r'(Debit Card|Credit Car d?|Credit Car|Online|Cash|Gift Card)\s*'
    r'(Shipped|Cancelled|Returned|Delivered|Pending)\s+'
    r'(TRK\d+)\s+'
    r'(\d+)\s*'
    r'(SAVE10|FREESHIP|WINTER15)?\s*'
    r'(Instagram|Referral|Email|Facebook|Google)\s+'
    r'([\d.]+)'
)

cols = ["OrderID", "Date", "CustomerID", "Product", "Quantity", "UnitPrice",
        "ShippingAddress", "PaymentMethod", "OrderStatus", "TrackingNumber",
        "ItemsInCart", "CouponCode", "ReferralSource", "TotalPrice"]

rows = [list(m.groups()) for line in text.split("\n")
        if line.strip().startswith("ORD")
        for m in [row_pattern.match(line.strip())] if m]

df = pd.DataFrame(rows, columns=cols)

df["PaymentMethod"] = df["PaymentMethod"].str.strip().replace(
    {"Credit Car": "Credit Card", "Credit Car d": "Credit Card"}
)

for col in ["Quantity", "UnitPrice", "ItemsInCart", "TotalPrice"]:
    df[col] = pd.to_numeric(df[col], errors="coerce")

df["Date_Incomplete"] = df["Date"]
df["Date"] = pd.NaT
df["CouponCode"] = df["CouponCode"].replace("", "NoCoupon").fillna("NoCoupon")

df.to_csv("clean_orders_data.csv", index=False)
