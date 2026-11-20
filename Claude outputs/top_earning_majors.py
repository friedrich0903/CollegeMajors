"""
Question: Which five college majors have the highest median earnings?
Do these majors also have low unemployment rates?

Data: FiveThirtyEight recent-grads.csv (ACS 2010-2012, graduates under 28).
Outputs: results.txt (printed tables) and three charts in charts/.
"""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

URL = ("https://raw.githubusercontent.com/fivethirtyeight/data/"
       "master/college-majors/recent-grads.csv")
LOCAL = Path("recent-grads.csv")

BLUE = "#2a78d6"      # top-5 majors
GRAY = "#b4b2ac"      # all other majors
INK = "#0b0b0b"
INK_2 = "#52514e"

# ---------------------------------------------------------------- data
df = pd.read_csv(LOCAL if LOCAL.exists() else URL)

top5 = (df.sort_values("Median", ascending=False, kind="stable")
          .head(5)[["Major", "Major_category", "Median",
                    "Unemployment_rate", "Sample_size"]])

median_unemp = df["Unemployment_rate"].median()
mean_unemp = df["Unemployment_rate"].mean()

df["Unemp_percentile"] = df["Unemployment_rate"].rank(pct=True) * 100
top5 = top5.join(df["Unemp_percentile"])
top5["Below_median_unemp"] = top5["Unemployment_rate"] < median_unemp

cutoff = top5["Median"].min()
ties = df[(df["Median"] == cutoff) & (~df["Major"].isin(top5["Major"]))]
corr = df["Median"].corr(df["Unemployment_rate"])

# ---------------------------------------------------------------- text output
lines = []
lines.append("Top 5 majors by median earnings")
lines.append(top5.to_string(index=False, formatters={
    "Median": "${:,.0f}".format,
    "Unemployment_rate": "{:.1%}".format,
    "Unemp_percentile": "{:.0f}".format,
}))
lines.append(f"\nMedian unemployment rate, all majors: {median_unemp:.1%}")
lines.append(f"Mean unemployment rate, all majors:   {mean_unemp:.1%}")
lines.append(f"Top-5 average unemployment rate:      "
             f"{top5['Unemployment_rate'].mean():.1%}")
if not ties.empty:
    lines.append(f"\nNote: tie at ${cutoff:,.0f} with: "
                 + ", ".join(ties["Major"])
                 + f" (unemployment {ties['Unemployment_rate'].iloc[0]:.1%})")
lines.append(f"\nCorrelation (median earnings vs unemployment), "
             f"all majors: {corr:.2f}")

report = "\n".join(lines)
print(report)
Path("results.txt").write_text(report + "\n")

# ---------------------------------------------------------------- charts
Path("charts").mkdir(exist_ok=True)
plt.rcParams.update({
    "font.size": 11,
    "axes.edgecolor": GRAY,
    "axes.labelcolor": INK_2,
    "xtick.color": INK_2,
    "ytick.color": INK_2,
    "axes.spines.top": False,
    "axes.spines.right": False,
})

short = (top5["Major"].str.title()
         .str.replace("Naval Architecture And Marine Engineering",
                      "Naval Arch. & Marine Eng.")
         .str.replace("Mining And Mineral Engineering",
                      "Mining & Mineral Eng."))
order = top5.assign(Short=short).iloc[::-1]   # largest at top

# Chart 1: median earnings of the top 5
fig, ax = plt.subplots(figsize=(8, 4))
ax.barh(order["Short"], order["Median"], color=BLUE, height=0.6)
for y, v in enumerate(order["Median"]):
    ax.text(v + 1500, y, f"${v:,.0f}", va="center", color=INK)
ax.set_xlim(0, order["Median"].max() * 1.18)
ax.xaxis.set_major_formatter(lambda x, _: f"${x/1000:.0f}k")
ax.set_title("Top 5 majors by median earnings", loc="left", color=INK)
ax.grid(axis="x", color="#e6e5e0")
ax.set_axisbelow(True)
fig.tight_layout()
fig.savefig("charts/1_top5_median_earnings.png", dpi=150)
plt.close(fig)

# Chart 2: unemployment of the top 5 vs the all-majors median
fig, ax = plt.subplots(figsize=(8, 4))
ax.barh(order["Short"], order["Unemployment_rate"], color=BLUE, height=0.6)
for y, v in enumerate(order["Unemployment_rate"]):
    ax.text(v + 0.002, y, f"{v:.1%}", va="center", color=INK)
ax.axvline(median_unemp, color=INK_2, linestyle="--", linewidth=1.5)
ax.text(median_unemp + 0.002, len(order) - 0.45,
        f"Median, all majors: {median_unemp:.1%}", color=INK_2)
ax.set_xlim(0, order["Unemployment_rate"].max() * 1.25)
ax.xaxis.set_major_formatter(lambda x, _: f"{x:.0%}")
ax.set_title("Unemployment rate of the top 5 earning majors",
             loc="left", color=INK)
ax.grid(axis="x", color="#e6e5e0")
ax.set_axisbelow(True)
fig.tight_layout()
fig.savefig("charts/2_top5_unemployment.png", dpi=150)
plt.close(fig)

# Chart 3: all majors, earnings vs unemployment, top 5 highlighted
is_top = df["Major"].isin(top5["Major"])
fig, ax = plt.subplots(figsize=(8, 5))
ax.scatter(df.loc[~is_top, "Unemployment_rate"], df.loc[~is_top, "Median"],
           s=28, color=GRAY, edgecolor="white", linewidth=0.6,
           label="Other majors")
ax.scatter(df.loc[is_top, "Unemployment_rate"], df.loc[is_top, "Median"],
           s=60, color=BLUE, edgecolor="white", linewidth=0.8,
           label="Top 5 by median earnings")
for _, r in order.iterrows():
    ax.annotate(r["Short"], (r["Unemployment_rate"], r["Median"]),
                xytext=(6, 2), textcoords="offset points",
                fontsize=9, color=INK)
ax.axvline(median_unemp, color=INK_2, linestyle="--", linewidth=1)
ax.xaxis.set_major_formatter(lambda x, _: f"{x:.0%}")
ax.yaxis.set_major_formatter(lambda y, _: f"${y/1000:.0f}k")
ax.set_xlabel("Unemployment rate")
ax.set_ylabel("Median earnings")
ax.set_title(f"Earnings vs unemployment, all 173 majors (r = {corr:.2f})",
             loc="left", color=INK)
ax.legend(frameon=False, loc="upper right")
ax.grid(color="#e6e5e0")
ax.set_axisbelow(True)
fig.tight_layout()
fig.savefig("charts/3_earnings_vs_unemployment.png", dpi=150)
plt.close(fig)

print("\nSaved results.txt and 3 charts in charts/")
