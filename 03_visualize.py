import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import os

PROCESSED_PATH = "data/processed/"
VISUALS_PATH = "visuals/"
os.makedirs(VISUALS_PATH, exist_ok=True)

MEMBER_COLOR = "#4C72B0"
CASUAL_COLOR = "#DD8452"
PALETTE = {"member": MEMBER_COLOR, "casual": CASUAL_COLOR}

plt.rcParams.update({"figure.dpi": 150, "axes.spines.top": False, "axes.spines.right": False, "axes.grid": True, "grid.alpha": 0.3})

daily_avg   = pd.read_csv(os.path.join(PROCESSED_PATH, "avg_ride_by_day.csv"))
daily_count = pd.read_csv(os.path.join(PROCESSED_PATH, "ride_count_by_day.csv"))
monthly     = pd.read_csv(os.path.join(PROCESSED_PATH, "monthly_trends.csv"))
bike_pref   = pd.read_csv(os.path.join(PROCESSED_PATH, "bike_type_pref.csv"))
hourly      = pd.read_csv(os.path.join(PROCESSED_PATH, "hourly_usage.csv"))

DAY_ORDER = ["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"]

fig, ax = plt.subplots(figsize=(10, 5))
for rtype, color in PALETTE.items():
    subset = daily_avg[daily_avg["member_casual"]==rtype]
    day_vals = [subset[d].values[0] if d in subset.columns else 0 for d in DAY_ORDER]
    ax.plot(DAY_ORDER, day_vals, marker="o", label=rtype.capitalize(), color=color, linewidth=2.5)
ax.set_title("Average Ride Duration by Day of Week", fontsize=14, fontweight="bold")
ax.set_xlabel("Day of Week")
ax.set_ylabel("Avg Ride Length (minutes)")
ax.legend(title="Rider Type")
plt.tight_layout()
plt.savefig(os.path.join(VISUALS_PATH, "01_avg_ride_by_day.png"))
plt.close()
print("Saved: 01_avg_ride_by_day.png")

fig, ax = plt.subplots(figsize=(10, 5))
x = range(len(DAY_ORDER))
width = 0.38
m_row = daily_count[daily_count["member_casual"]=="member"]
c_row = daily_count[daily_count["member_casual"]=="casual"]
m_vals = [m_row[d].values[0] if d in m_row.columns else 0 for d in DAY_ORDER]
c_vals = [c_row[d].values[0] if d in c_row.columns else 0 for d in DAY_ORDER]
ax.bar([i-width/2 for i in x], m_vals, width, label="Member", color=MEMBER_COLOR, alpha=0.85)
ax.bar([i+width/2 for i in x], c_vals, width, label="Casual", color=CASUAL_COLOR, alpha=0.85)
ax.set_xticks(list(x))
ax.set_xticklabels(DAY_ORDER)
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v,_: f"{int(v):,}"))
ax.set_title("Number of Rides by Day of Week", fontsize=14, fontweight="bold")
ax.set_xlabel("Day of Week")
ax.set_ylabel("Total Rides")
ax.legend(title="Rider Type")
plt.tight_layout()
plt.savefig(os.path.join(VISUALS_PATH, "02_ride_count_by_day.png"))
plt.close()
print("Saved: 02_ride_count_by_day.png")

MONTH_ORDER = ["January","February","March","April","May","June","July","August","September","October","November","December"]
fig, ax = plt.subplots(figsize=(12, 5))
for rtype, color in PALETTE.items():
    subset = monthly[monthly["rider_type"]==rtype].copy()
    subset["month"] = pd.Categorical(subset["month"], categories=MONTH_ORDER, ordered=True)
    subset = subset.sort_values("month")
    ax.plot(subset["month"], subset["ride_count"], marker="o", label=rtype.capitalize(), color=color, linewidth=2.5)
ax.set_title("Monthly Ride Volume - Casual vs Member", fontsize=14, fontweight="bold")
ax.set_xlabel("Month")
ax.set_ylabel("Total Rides")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v,_: f"{int(v):,}"))
plt.xticks(rotation=30)
ax.legend(title="Rider Type")
plt.tight_layout()
plt.savefig(os.path.join(VISUALS_PATH, "03_monthly_volume.png"))
plt.close()
print("Saved: 03_monthly_volume.png")

fig, ax = plt.subplots(figsize=(8, 5))
pivot_bike = bike_pref.pivot(index="rider_type", columns="bike_type", values="pct").fillna(0)
pivot_bike.plot(kind="bar", ax=ax, colormap="Set2", edgecolor="white")
ax.set_title("Bike Type Preference by Rider Type (%)", fontsize=14, fontweight="bold")
ax.set_xlabel("")
ax.set_ylabel("% of Rides")
ax.set_xticklabels(ax.get_xticklabels(), rotation=0)
ax.legend(title="Bike Type", bbox_to_anchor=(1.01,1))
plt.tight_layout()
plt.savefig(os.path.join(VISUALS_PATH, "04_bike_type_pref.png"))
plt.close()
print("Saved: 04_bike_type_pref.png")

hourly_pivot = hourly.pivot(index="rider_type", columns="hour", values="ride_count").fillna(0)
fig, ax = plt.subplots(figsize=(14, 3))
sns.heatmap(hourly_pivot, ax=ax, cmap="YlOrRd", linewidths=0.3, linecolor="white", cbar_kws={"label": "Ride Count"})
ax.set_title("Rides by Hour of Day - Heatmap", fontsize=14, fontweight="bold")
ax.set_xlabel("Hour of Day (0 = midnight)")
ax.set_ylabel("")
plt.tight_layout()
plt.savefig(os.path.join(VISUALS_PATH, "05_hourly_heatmap.png"))
plt.close()
print("Saved: 05_hourly_heatmap.png")

print("\nAll 5 charts saved to visuals/ folder. Ready for Power BI!")
