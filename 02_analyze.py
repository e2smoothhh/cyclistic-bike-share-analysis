import pandas as pd
import numpy as np
import os

PROCESSED_PATH = "data/processed/"
os.makedirs(PROCESSED_PATH, exist_ok=True)

df = pd.read_csv(os.path.join(PROCESSED_PATH, "cyclistic_clean.csv"),
                 parse_dates=["started_at", "ended_at"])

print(f"Loaded clean dataset: {df.shape}")
print(f"Date range: {df['started_at'].min().date()} to {df['started_at'].max().date()}")

print("\n=== RIDE LENGTH SUMMARY (minutes) by Member Type ===")
summary = df.groupby("member_casual")["ride_length_min"].agg(
    count="count", mean="mean", median="median", std="std", min="min", max="max"
).round(2)
print(summary)

DAY_ORDER = ["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"]

print("\n=== Avg Ride Length by Day & Member Type ===")
pivot_day = df.pivot_table(
    index="member_casual", columns="day_name",
    values="ride_length_min", aggfunc="mean"
)[DAY_ORDER].round(2)
print(pivot_day)

print("\n=== Ride Count by Day & Member Type ===")
pivot_count = df.pivot_table(
    index="member_casual", columns="day_name",
    values="ride_id", aggfunc="count"
)[DAY_ORDER]
print(pivot_count)

print("\n=== Monthly Ride Counts ===")
monthly = df.groupby(["year","month_name","member_casual"])["ride_id"].count().reset_index()
monthly.columns = ["year","month","rider_type","ride_count"]
print(monthly.sort_values(["year","month"]).to_string(index=False))

print("\n=== Bike Type by Member Type ===")
bike_pref = df.groupby(["member_casual","rideable_type"])["ride_id"].count().reset_index()
bike_pref.columns = ["rider_type","bike_type","count"]
bike_pref["pct"] = bike_pref.groupby("rider_type")["count"].transform(
    lambda x: (x / x.sum() * 100).round(1))
print(bike_pref.sort_values(["rider_type","count"], ascending=[True,False]))

print("\n=== Rides by Hour of Day ===")
hourly = df.groupby(["member_casual","hour"])["ride_id"].count().reset_index()
hourly.columns = ["rider_type","hour","ride_count"]
print(hourly.to_string(index=False))

print("\n=== Top 10 Start Stations - Casual Riders ===")
top_stations = (df[df["member_casual"]=="casual"]
    .groupby("start_station_name")["ride_id"].count()
    .sort_values(ascending=False).head(10).reset_index())
top_stations.columns = ["station","ride_count"]
print(top_stations.to_string(index=False))

exports = {
    "summary_stats.csv": summary.reset_index(),
    "avg_ride_by_day.csv": pivot_day.reset_index(),
    "ride_count_by_day.csv": pivot_count.reset_index(),
    "monthly_trends.csv": monthly,
    "bike_type_pref.csv": bike_pref,
    "hourly_usage.csv": hourly,
    "top_stations_casual.csv": top_stations,
}

for fname, data in exports.items():
    path = os.path.join(PROCESSED_PATH, fname)
    data.to_csv(path, index=False)
    print(f"Exported: {path}")

print("\nAll summary tables exported. Ready for Power BI import.")
