import pandas as pd
import numpy as np
import os
import glob

RAW_PATH = "data/raw/"
PROCESSED_PATH = "data/processed/"
os.makedirs(PROCESSED_PATH, exist_ok=True)

csv_files = sorted(glob.glob(os.path.join(RAW_PATH, "*.csv")))
print(f"Found {len(csv_files)} CSV files.")

df_list = []
for f in csv_files:
    temp = pd.read_csv(f, low_memory=False)
    df_list.append(temp)

df = pd.concat(df_list, ignore_index=True)
print(f"Raw combined shape: {df.shape}")
print(f"Columns: {list(df.columns)}")

print("\n--- Data Types ---")
print(df.dtypes)
print("\n--- Null Counts ---")
print(df.isnull().sum())

df["started_at"] = pd.to_datetime(df["started_at"])
df["ended_at"]   = pd.to_datetime(df["ended_at"])

df["ride_length_min"] = (df["ended_at"] - df["started_at"]).dt.total_seconds() / 60

df["day_of_week"] = df["started_at"].dt.day_of_week.map(
    {0:2, 1:3, 2:4, 3:5, 4:6, 5:7, 6:1}
)
df["day_name"]   = df["started_at"].dt.day_name()
df["month"]      = df["started_at"].dt.month
df["month_name"] = df["started_at"].dt.strftime("%B")
df["hour"]       = df["started_at"].dt.hour
df["year"]       = df["started_at"].dt.year

def get_season(month):
    if month in [12, 1, 2]:  return "Winter"
    elif month in [3, 4, 5]: return "Spring"
    elif month in [6, 7, 8]: return "Summer"
    else:                     return "Fall"

df["season"] = df["month"].apply(get_season)

before = len(df)
df = df[df["ride_length_min"] > 0]
df = df[df["ride_length_min"] >= 1]
df = df[df["ride_length_min"] <= 1440]
df = df.dropna(subset=["start_station_name", "end_station_name"])
df = df.drop_duplicates(subset=["ride_id"])
after = len(df)

print(f"\nRows removed during cleaning: {before - after:,}")
print(f"Clean dataset shape: {df.shape}")
print("\n--- Rider Type Distribution ---")
print(df["member_casual"].value_counts())

output_path = os.path.join(PROCESSED_PATH, "cyclistic_clean.csv")
df.to_csv(output_path, index=False)
print(f"\nCleaned file saved to: {output_path}")
