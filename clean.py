"""
Project 1: Data Cleaning & Preparation
Extracts and cleans order data from Dataset_for_Data_Analytics.pdf.

The dataset was provided as a PDF, not a CSV/Excel file. Text extraction
revealed the source data itself has two built-in defects (not caused by
extraction):
  1. Every 'Date' value is missing its final digit
     (e.g. "2023-01-0" instead of a full date like "2023-01-06").
  2. "Credit Card" is consistently truncated to "Credit Car" and fused
     directly onto the next field with no separating space.

Because the categorical fields in this dataset are limited (5 products,
5 order statuses, 5 payment methods, etc.), regex pattern-matching
against known vocabularies is used to correctly split each row instead
of relying on column position, which would corrupt the data further.
"""

import re
import pandas as pd

# Step 1: extract raw text from the PDF (layout mode preserves spacing)
# Run this once from the command line before running this script:
#   pdftotext -layout Dataset_for_Data_Analytics.pdf sample.txt

with open("sample.txt") as f:
    text = f.read()

# Step 2: parse each order row using known field vocabularies
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

rows = []
for line in text.split("\n"):
    line = line.strip()
    if not line.startswith("ORD"):
        continue
    m = row_pattern.match(line)
    if m:
        rows.append(list(m.groups()))

df = pd.DataFrame(rows, columns=cols)
df.to_csv("raw_orders_data.csv", index=False)

print("Raw rows parsed:", len(df))

# Step 3: clean the parsed data
df_clean = df.copy()

# Fix truncated "Credit Car" -> "Credit Card"
df_clean["PaymentMethod"] = df_clean["PaymentMethod"].str.strip().replace({
    "Credit Car": "Credit Card",
    "Credit Car d": "Credit Card"
})

# Rebuild shipping address
df_clean["ShippingAddress"] = df_clean["ShippingAddress"] + " Main St"

# Convert numeric columns
for col in ["Quantity", "UnitPrice", "ItemsInCart", "TotalPrice"]:
    df_clean[col] = pd.to_numeric(df_clean[col], errors="coerce")

# Dates are missing their final digit in the SOURCE file -> unrecoverable.
# Keep the truncated raw value for reference, but treat Date as missing
# rather than guessing the final digit.
df_clean["Date_Incomplete"] = df_clean["Date"]
df_clean["Date"] = pd.NaT

# Missing coupon codes -> explicit label instead of blank
df_clean["CouponCode"] = df_clean["CouponCode"].replace("", "NoCoupon").fillna("NoCoupon")

# Step 4: verification checks
print("Duplicate rows:", df_clean.duplicated().sum())

expected_total = (df_clean["Quantity"] * df_clean["UnitPrice"]).round(2)
mismatches = (expected_total - df_clean["TotalPrice"]).abs() > 0.05
print("Rows where TotalPrice doesn't match Quantity x UnitPrice:", mismatches.sum())

# Step 5: save cleaned data
df_clean.to_csv("clean_orders_data.csv", index=False)

print(f"\nCleaning complete. Rows: {len(df_clean)}")
print("Remaining missing values:")
print(df_clean.isnull().sum())
