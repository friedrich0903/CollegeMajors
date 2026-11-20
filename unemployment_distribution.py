"""
Question: What does the distribution of unemployment rates across college majors look like?
Dataset: recent-grads.csv (one row per college major)
"""

import pandas as pd
import matplotlib.pyplot as plt

# 1. Load the data
df = pd.read_csv("recent-grads.csv")
rates = df["Unemployment_rate"] * 100  # convert to percent

# 2. Summary statistics
print("Number of majors:", len(rates))
print(f"Mean:    {rates.mean():.2f}%")
print(f"Median:  {rates.median():.2f}%")
print(f"Std dev: {rates.std():.2f}%")
print(f"Min:     {rates.min():.2f}%")
print(f"25th percentile: {rates.quantile(0.25):.2f}%")
print(f"75th percentile: {rates.quantile(0.75):.2f}%")
print(f"Max:     {rates.max():.2f}%")
print(f"Skewness: {rates.skew():.2f}")

# 3. Majors at the extremes
cols = ["Major", "Major_category", "Unemployment_rate"]
print("\nHighest unemployment rates:")
print(df.nlargest(5, "Unemployment_rate")[cols].to_string(index=False))
print("\nLowest unemployment rates:")
print(df.nsmallest(5, "Unemployment_rate")[cols].to_string(index=False))

# 4. Plots: histogram and boxplot
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(9, 7), sharex=True,
                               gridspec_kw={"height_ratios": [3, 1]})

ax1.hist(rates, bins=20, color="steelblue", edgecolor="white")
ax1.axvline(rates.mean(), color="red", linestyle="--",
            label=f"Mean = {rates.mean():.1f}%")
ax1.axvline(rates.median(), color="orange", linestyle="-",
            label=f"Median = {rates.median():.1f}%")
ax1.set_ylabel("Number of majors")
ax1.set_title("Distribution of unemployment rates across college majors")
ax1.legend()

ax2.boxplot(rates, orientation="horizontal", widths=0.6)
ax2.set_yticks([])
ax2.set_xlabel("Unemployment rate (%)")

plt.tight_layout()
plt.savefig("unemployment_distribution.png", dpi=150)
plt.show()
