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

df = pd.read_csv("SP500_financials2006-2009")
df.set_index('Date', inplace=True)
df.fillna(0, inplace=True)

###: dropping stocks with values of 0 throughout period
for stock in df.columns.values.tolist():
    means = np.mean(df[stock])
    if means == 0:
        df.drop(stock, axis=1, inplace=True)
stocks = df.columns.values.tolist()

def set_years():

    df.reset_index(inplace=True)

    df_2006 = df[df['Date'] < '2006-12-31']
    df_2007 = df[df['Date'] > '2006-12-31']
    df_2007 = df_2007['Date'] < '2007-12-31'
    df_2008 = df[df['Date'] > '2007-12-31']
    df_2008 = df_2008['Date'] < '2008-12-31'
    df_2009 = df[df['Date'] > '2008-12-31']
    df_2009 = df_2009['Date'] < '2009-12-31'

    return df_2006, df_2007, df_2008, df_2009

set_years()

def annualized_returns():

    df_2006, df_2007, df_2008, df_2009 = set_years()
    each_alloc = 1 / len(stocks)
    alloc = np.full((1, len(stocks)), each_alloc)

    ##: 2006 returns
    df_2006.set_index('Date', inplace=True)
    df_2006.drop('index', axis=1, inplace=True)
    df_2006.fillna(0, inplace=True)
    list = []
    for stock in df_2006:
        vals_2006 = df_2006[stock].values.copy()
        pct_change_2006 = (vals_2006 / vals_2006[0])
        for i in pct_change_2006:
            sub = pct_change_2006[-1] - pct_change_2006[0]
            list.append(sub)
    print(list)

        # pct_change is 116row x 59col, alloc is 1row x 59col
        # returns = np.dot(pct_change_2006, alloc.reshape(59,1))

        # will return 116 x 1 matrix for each equity in portfolio

annualized_returns()
