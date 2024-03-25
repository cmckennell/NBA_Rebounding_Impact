import pandas as pd
import numpy as np
from scipy.stats import ttest_ind, chi2_contingency

df = pd.read_excel('Team Stats 2023.xlsx')
df['Rebound Differential'] = df['Team TRB'] - df['Opponent TRB']
# print(df.columns)


# Separate the data into two groups based on the categorical variable
group1 = df[df['W/L'] == 'W']['Team TRB'].to_list()
group2 = df[df['W/L'] == 'L']['Team TRB'].to_list() 

# Output the means of each group
print(np.mean(group1))
print(np.mean(group2))


# Perform the two-sample t-test
t_stat, p_value = ttest_ind(group1, group2)

# Output the results
print(f"T-statistic: {t_stat}")
print(f"P-value: {p_value}")

import matplotlib.pyplot as plt

# Create a boxplot
plt.boxplot([group1, group2], labels=['Wins', 'Losses'])
plt.xlabel('Game Result')
plt.ylabel('Rebound Total')
plt.title('Rebound Total for Wins and Losses')
plt.show()
plt.clf()