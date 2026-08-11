"""
Project 1: Data Cleaning & Preparation
Cleans raw_employee_data.csv by handling missing values, duplicates,
and inconsistent formatting (dates, numbers, text).
"""

import pandas as pd

# Load raw data
df = pd.read_csv("raw_employee_data.csv")

# 1. Identify missing values
print("Missing values per column:")
print(df.isnull().sum())

# 2. Remove duplicate rows
df_clean = df.drop_duplicates(
    subset=["name", "age", "city", "join_date", "salary", "email"]
).copy()

# 3. Fix text formatting (standardize case, strip whitespace)
df_clean["name"] = df_clean["name"].str.strip().str.title()
df_clean["city"] = df_clean["city"].str.strip().str.title()
df_clean["email"] = df_clean["email"].str.strip().str.lower()

# 4. Fix numeric formatting (age, salary)
df_clean["age"] = pd.to_numeric(df_clean["age"], errors="coerce")
df_clean["salary"] = df_clean["salary"].astype(str).str.replace(",", "", regex=False)
df_clean["salary"] = pd.to_numeric(df_clean["salary"], errors="coerce")

# 5. Fix date formatting (multiple formats -> one standard)
df_clean["join_date"] = pd.to_datetime(
    df_clean["join_date"], errors="coerce", format="mixed"
)

# 6. Handle remaining missing values
df_clean["age"] = df_clean["age"].fillna(df_clean["age"].median())
df_clean["salary"] = df_clean["salary"].fillna(df_clean["salary"].median())
df_clean["city"] = df_clean["city"].fillna("Unknown")
df_clean["email"] = df_clean["email"].fillna("unknown@mail.com")
# join_date left as NaT where missing -- no reliable way to infer it

# Save cleaned data
df_clean.to_csv("clean_employee_data.csv", index=False)

print("\nCleaning complete.")
print(f"Rows before: {len(df)} | Rows after: {len(df_clean)}")
print("Remaining missing values:")
print(df_clean.isnull().sum())
