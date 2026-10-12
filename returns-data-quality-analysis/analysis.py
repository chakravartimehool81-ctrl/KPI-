from pathlib import Path
import sys
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(sys.executable).parent if getattr(sys, "frozen", False) else Path(__file__).parent
DATA_DIR = Path(getattr(sys, "_MEIPASS", ROOT)) / "data"
OUT = ROOT / "outputs"
OUT.mkdir(exist_ok=True)
raw = pd.read_csv(DATA_DIR / "orders_and_returns.csv")
quality = pd.DataFrame({"check": ["rows", "duplicate_order_ids", "missing_product_ids"], "value": [len(raw), raw.duplicated("order_id").sum(), raw["product_id"].isna().sum()]})
clean = raw.drop_duplicates("order_id").dropna(subset=["product_id"]).copy()
quality.to_csv(OUT / "data_quality_report.csv", index=False)
rates = clean.groupby("category").agg(orders=("order_id", "nunique"), returns=("returned", "sum"), avg_delivery_days=("delivery_days", "mean"))
rates["return_rate"] = rates["returns"] / rates["orders"]
rates.sort_values("return_rate", ascending=False).to_csv(OUT / "return_rate_by_category.csv")
reasons = clean.loc[clean.returned.eq(1), "return_reason"].value_counts()
reasons.to_csv(OUT / "return_reasons.csv", header=["returns"])
fig, axes = plt.subplots(1, 2, figsize=(11,4.5))
axes[0].bar(rates.index, rates["return_rate"] * 100, color="#e15759")
axes[0].set_title("Return Rate by Category")
axes[0].set_ylabel("Percent")
axes[0].tick_params(axis="x", rotation=25)
axes[1].barh(reasons.index, reasons.values, color="#4e79a7")
axes[1].set_title("Top Return Reasons")
fig.tight_layout()
fig.savefig(OUT / "returns_analysis.png", dpi=160)
print(quality.to_string(index=False))
if getattr(sys, "frozen", False):
    input("Analysis complete. Results are in the outputs folder. Press Enter to close...")
