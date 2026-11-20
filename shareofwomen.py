import pandas as pd
from scipy.stats import linregress

import matplotlib.pyplot as plt

from pathlib import Path
data = pd.read_csv(Path(__file__).parent / 'recent-grads.csv').dropna(subset=['ShareWomen', 'Median'])

share_women = data['ShareWomen']
median_earnings = data['Median']

slope, intercept, r_value, p_value, std_err = linregress(share_women, median_earnings)

print(f"Slope: {slope}")
print(f"Intercept: {intercept}")
print(f"R-squared: {r_value**2}")

plt.scatter(share_women, median_earnings, alpha=0.5, label='Data points')
plt.plot(share_women, slope * share_women + intercept, color='red', label='Regression line')
plt.xlabel('Share of Women in Major')
plt.ylabel('Median Earnings')
plt.title('Relationship Between Share of Women and Median Earnings')
plt.legend()
plt.show()