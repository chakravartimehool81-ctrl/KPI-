from pathlib import Path
import sys
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(sys.executable).parent if getattr(sys, "frozen", False) else Path(__file__).parent
DATA_DIR = Path(getattr(sys, "_MEIPASS", ROOT)) / "data"
OUT = ROOT / "outputs"
OUT.mkdir(exist_ok=True)
df = pd.read_csv(DATA_DIR / "retail_sales.csv", parse_dates=["order_date"])
df["revenue"] = df["quantity"] * df["unit_price"] * (1 - df["discount"])
df["month"] = df["order_date"].dt.to_period("M").astype(str)
monthly = df.groupby("month", as_index=False)["revenue"].sum()
regional = df.groupby("region", as_index=False).agg(revenue=("revenue", "sum"), orders=("order_id", "nunique"))
category = df.groupby("category", as_index=False)["revenue"].sum().sort_values("revenue", ascending=False)
monthly.to_csv(OUT / "monthly_revenue.csv", index=False)
regional.to_csv(OUT / "regional_performance.csv", index=False)
category.to_csv(OUT / "category_performance.csv", index=False)
fig, axes = plt.subplots(1, 2, figsize=(12, 4.8))
axes[0].plot(monthly["month"], monthly["revenue"], marker="o", color="#2f6fed")
axes[0].set_title("Monthly Revenue")
axes[0].tick_params(axis="x", rotation=45)
axes[0].grid(alpha=.25)
axes[1].bar(regional["region"], regional["revenue"], color="#f28e2b")
axes[1].set_title("Revenue by Region")
fig.tight_layout()
fig.savefig(OUT / "sales_dashboard.png", dpi=160)
print(f"Revenue: {df.revenue.sum():,.0f}; top category: {category.iloc[0].category}; top region: {regional.loc[regional.revenue.idxmax(), 'region']}")
if getattr(sys, "frozen", False):
    input("Analysis complete. Results are in the outputs folder. Press Enter to close...")
