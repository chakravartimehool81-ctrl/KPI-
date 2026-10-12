from pathlib import Path
import sys
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(sys.executable).parent if getattr(sys, "frozen", False) else Path(__file__).parent
DATA_DIR = Path(getattr(sys, "_MEIPASS", ROOT)) / "data"
OUT = ROOT / "outputs"
OUT.mkdir(exist_ok=True)
df = pd.read_csv(DATA_DIR / "monthly_kpis.csv")
df["conversion_rate"] = df["orders"] / df["website_visitors"]
df["revenue"] = df["orders"] * df["average_order_value"]
df["revenue_growth_pct"] = df["revenue"].pct_change() * 100
df.to_csv(OUT / "kpi_scorecard.csv", index=False)
latest = df.iloc[-1]
previous = df.iloc[-2]
summary = pd.DataFrame({
    "kpi": ["Revenue", "Orders", "Conversion Rate", "Customer Satisfaction"],
    "latest": [latest.revenue, latest.orders, latest.conversion_rate, latest.customer_satisfaction],
    "change_vs_previous_pct": [(latest.revenue/previous.revenue-1)*100, (latest.orders/previous.orders-1)*100, (latest.conversion_rate/previous.conversion_rate-1)*100, (latest.customer_satisfaction/previous.customer_satisfaction-1)*100]
})
summary.to_csv(OUT / "executive_summary.csv", index=False)
fig, axes = plt.subplots(2, 2, figsize=(11,7))
series = [("revenue", "Revenue", "#4e79a7"), ("orders", "Orders", "#f28e2b"), ("conversion_rate", "Conversion Rate", "#59a14f"), ("customer_satisfaction", "Customer Satisfaction", "#b07aa1")]
for ax, (col, title, color) in zip(axes.flat, series):
    ax.plot(df["month"], df[col], marker="o", color=color)
    ax.set_title(title)
    ax.tick_params(axis="x", rotation=45)
    ax.grid(alpha=.2)
fig.tight_layout()
fig.savefig(OUT / "executive_kpi_dashboard.png", dpi=160)
print(summary.to_string(index=False))
if getattr(sys, "frozen", False):
    input("Analysis complete. Results are in the outputs folder. Press Enter to close...")
