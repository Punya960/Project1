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
