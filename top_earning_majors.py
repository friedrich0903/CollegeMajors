"""
Question: Which five college majors have the highest median earnings?
Do these majors also have low unemployment rates?

Data: FiveThirtyEight recent-grads.csv (ACS 2010-2012, graduates under 28).
"""

import pandas as pd

URL = ("https://raw.githubusercontent.com/fivethirtyeight/data/"
       "master/college-majors/recent-grads.csv")

df = pd.read_csv(URL)

# Top 5 majors by median earnings
top5 = (df.sort_values("Median", ascending=False, kind="stable")
          .head(5)[["Major", "Major_category", "Median",
                    "Unemployment_rate", "Sample_size"]])

# Benchmarks across all 173 majors
median_unemp = df["Unemployment_rate"].median()
mean_unemp = df["Unemployment_rate"].mean()

# Where each top-5 major sits in the unemployment distribution
# (percentile 0 = lowest unemployment, 100 = highest)
df["Unemp_percentile"] = df["Unemployment_rate"].rank(pct=True) * 100
top5 = top5.join(df["Unemp_percentile"])
top5["Below_median_unemp"] = top5["Unemployment_rate"] < median_unemp

pd.set_option("display.width", 140)
print("Top 5 majors by median earnings")
print(top5.to_string(index=False, formatters={
    "Median": "${:,.0f}".format,
    "Unemployment_rate": "{:.1%}".format,
    "Unemp_percentile": "{:.0f}".format,
}))

print(f"\nMedian unemployment rate, all majors: {median_unemp:.1%}")
print(f"Mean unemployment rate, all majors:   {mean_unemp:.1%}")
print(f"Top-5 average unemployment rate:      "
      f"{top5['Unemployment_rate'].mean():.1%}")

# Tie check: does a 6th major share the 5th-highest salary?
cutoff = top5["Median"].min()
ties = df[(df["Median"] == cutoff) & (~df["Major"].isin(top5["Major"]))]
if not ties.empty:
    print(f"\nNote: tie at ${cutoff:,.0f} with: "
          + ", ".join(ties["Major"])
          + f" (unemployment {ties['Unemployment_rate'].iloc[0]:.1%})")

# Correlation between pay and unemployment across all majors
corr = df["Median"].corr(df["Unemployment_rate"])
print(f"\nCorrelation (median earnings vs unemployment), all majors: {corr:.2f}")
