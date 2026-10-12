from pathlib import Path
import sys
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(sys.executable).parent if getattr(sys, "frozen", False) else Path(__file__).parent
DATA_DIR = Path(getattr(sys, "_MEIPASS", ROOT)) / "data"
OUT = ROOT / "outputs"
OUT.mkdir(exist_ok=True)
df = pd.read_csv(DATA_DIR / "regional_demand.csv")
summary = df.groupby("region", as_index=False).agg(total_orders=("orders", "sum"), avg_conversion=("conversion_rate", "mean"), avg_rating=("customer_rating", "mean"))
summary["demand_index"] = 100 * summary["total_orders"] / summary["total_orders"].max()
summary["opportunity_score"] = .55 * summary["demand_index"] + .45 * (100 * summary["avg_conversion"] / summary["avg_conversion"].max())
summary = summary.sort_values("opportunity_score", ascending=False)
summary.to_csv(OUT / "regional_opportunity_ranking.csv", index=False)
pivot = df.pivot_table(index="month", columns="region", values="orders", aggfunc="sum")
pivot.to_csv(OUT / "monthly_orders_by_region.csv")
ax = pivot.plot(figsize=(10,5), marker="o")
ax.set_title("Monthly Orders by Region")
ax.set_ylabel("Orders")
ax.grid(alpha=.25)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(OUT / "regional_demand_trend.png", dpi=160)
print(summary.to_string(index=False))
if getattr(sys, "frozen", False):
    input("Analysis complete. Results are in the outputs folder. Press Enter to close...")
