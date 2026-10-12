from pathlib import Path
import sys
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(sys.executable).parent if getattr(sys, "frozen", False) else Path(__file__).parent
DATA_DIR = Path(getattr(sys, "_MEIPASS", ROOT)) / "data"
OUT = ROOT / "outputs"
OUT.mkdir(exist_ok=True)
df = pd.read_csv(DATA_DIR / "transactions.csv", parse_dates=["invoice_date"])
snapshot = pd.Timestamp("2026-01-01")
rfm = df.groupby("customer_id").agg(
    recency=("invoice_date", lambda x: (snapshot - x.max()).days),
    frequency=("invoice_id", "nunique"), monetary=("amount", "sum")
).reset_index()
rfm["r_score"] = pd.qcut(rfm["recency"].rank(method="first"), 4, labels=[4,3,2,1]).astype(int)
rfm["f_score"] = pd.qcut(rfm["frequency"].rank(method="first"), 4, labels=[1,2,3,4]).astype(int)
rfm["m_score"] = pd.qcut(rfm["monetary"].rank(method="first"), 4, labels=[1,2,3,4]).astype(int)
score = rfm[["r_score", "f_score", "m_score"]].sum(axis=1)
rfm["segment"] = pd.cut(score, bins=[0,5,8,10,12], labels=["At Risk", "Regular", "Loyal", "Champions"])
rfm.to_csv(OUT / "customer_segments.csv", index=False)
counts = rfm["segment"].value_counts().sort_index()
counts.to_csv(OUT / "segment_summary.csv", header=["customers"])
ax = counts.plot(kind="bar", color=["#e15759", "#76b7b2", "#59a14f", "#4e79a7"], figsize=(8,5))
ax.set_title("Customer Segments")
ax.set_xlabel("")
ax.set_ylabel("Customers")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig(OUT / "rfm_segments.png", dpi=160)
print(counts.to_string())
if getattr(sys, "frozen", False):
    input("Analysis complete. Results are in the outputs folder. Press Enter to close...")
