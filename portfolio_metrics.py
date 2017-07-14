"""
Assumptions of 'financial index':
1) even weighting distribution of each equity in portfolio
2) equities were held from dt_start ('2006-05-06') to dt_end ('2009-01-01')
3) all calculations are based on those time periods
"""

import pandas as pd
import numpy as np
import datetime as dt
import pandas_datareader.data as web
import matplotlib.pyplot as plt
from matplotlib import style
import warnings
warnings.filterwarnings('ignore')

df = pd.read_csv("SP500_joined_closes_2.csv")
df.fillna(0, inplace=True)
no_index = df.drop('Date', axis=1)
stocks = no_index.columns.values.tolist()

for stock in stocks:
    print("{} 3yr mean: ".format(stock), np.mean(no_index[stock]))

all_standard_deviations = []
stds = np.std(no_index)
for std in stds:
    all_standard_deviations.append(std)
print("Standard Deviation of all stocks: ", np.std(all_standard_deviations))

###: WANTED PORTFOLIO METRICS
# SPLIT FROM 2006 - right before crash TO crash till 2009
# Return from 2006 till before the crash (do it by dates)
# Sharpe Ratio
# Roy's Safety-First Ratio
# Sortino Ratio
# Treynor Ratio
# Information Ratio

