# Project1
Data cleaning
import pandas as pd
import numpy as np

df = pd.read_csv("raw_employee_data.csv")

# 1. Identify missing values
print(df.isnull().sum())

# 2. Remove duplicates
df = df.drop_duplicates(subset=["name","age","city","join_date","salary","email"])

# 3. Fix text formatting (standardize case, strip whitespace)
df["name"] = df["name"].str.strip().str.title()
df["city"] = df["city"].str.strip().str.title()
df["email"] = df["email"].str.strip().str.lower()

# 4. Fix numbers (age, salary — strip symbols, convert to numeric)
df["age"] = pd.to_numeric(df["age"], errors="coerce")
df["salary"] = df["salary"].astype(str).str.replace(",", "", regex=False)
df["salary"] = pd.to_numeric(df["salary"], errors="coerce")

# 5. Fix dates (multiple formats -> one standard)
df["join_date"] = pd.to_datetime(df["join_date"], errors="coerce", format="mixed")

# 6. Handle remaining missing values (example: fill or flag)
df["age"] = df["age"].fillna(df["age"].median())
df["city"] = df["city"].fillna("Unknown")

df.to_csv("clean_employee_data.csv", index=False)
# Project 1: Data Cleaning & Preparation

## Goal
Clean a raw employee dataset by handling missing values, duplicates, and
inconsistent data formats (dates, numbers, text) using Python (pandas).

## Files
- `raw_employee_data.csv` — original, messy dataset
- `clean_employee_data.csv` — cleaned output
- `clean.py` — cleaning script

## Issues Found in Raw Data
- **Missing values:** age (11), city (9), join_date (11), salary (18), email (23)
- **Duplicates:** 6 exact duplicate rows
- **Inconsistent formatting:**
  - Names/cities in mixed case ("jane doe", "LOS ANGELES")
  - Salary stored as text with commas or "N/A" (e.g. "58,000")
  - Dates in multiple formats (`2023-01-15`, `15/02/2023`, `2023.03.10`)
  - Emails with extra whitespace/inconsistent case

## Cleaning Steps
1. **Duplicates** — dropped 6 exact duplicate rows using `drop_duplicates()`
2. **Text formatting** — standardized name/city casing with `.str.title()`,
   lowercased and stripped emails
3. **Numeric formatting** — stripped commas from salary, converted salary/age
   to numeric with `pd.to_numeric(errors="coerce")`
4. **Date formatting** — parsed mixed date formats into one standard format
   using `pd.to_datetime(format="mixed")`
5. **Missing values** — filled age/salary with median values, city/email
   with placeholder text ("Unknown" / "unknown@mail.com")
   - `join_date` nulls were **left blank intentionally** rather than filled,
     since there's no reliable way to infer a missing join date

## Result
- Rows: 66 → 60 (after removing duplicates)
- All missing values resolved except `join_date`, which was left null by design

```python
import pandas as pd

df = pd.read_csv("raw_employee_data.csv")

df_clean = df.drop_duplicates(
    subset=["name","age","city","join_date","salary","email"]
).copy()

df_clean["name"] = df_clean["name"].str.strip().str.title()
df_clean["city"] = df_clean["city"].str.strip().str.title()
df_clean["email"] = df_clean["email"].str.strip().str.lower()

df_clean["age"] = pd.to_numeric(df_clean["age"], errors="coerce")
df_clean["salary"] = df_clean["salary"].astype(str).str.replace(",", "", regex=False)
df_clean["salary"] = pd.to_numeric(df_clean["salary"], errors="coerce")

df_clean["join_date"] = pd.to_datetime(df_clean["join_date"], errors="coerce", format="mixed")

df_clean["age"] = df_clean["age"].fillna(df_clean["age"].median())
df_clean["salary"] = df_clean["salary"].fillna(df_clean["salary"].median())
df_clean["city"] = df_clean["city"].fillna("Unknown")
df_clean["email"] = df_clean["email"].fillna("unknown@mail.com")

df_clean.to_csv("clean_employee_data.csv", index=False)
