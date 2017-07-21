###: INCOMPLETE

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
from math import isnan
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
    df_07 = df[df['Date'] > '2006-12-31']
    df_2007 = pd.DataFrame([df_07['Date'] < '2007-12-31'])
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

    ###: 2006 returns
    df_2006.set_index('Date', inplace=True)
    df_2006.drop('index', axis=1, inplace=True)
    df_2006.fillna(0, inplace=True)
    yrly_pct_change06 = []
    for stock in df_2006:
        vals = df_2006[stock].values.copy()
        pct_change = vals / vals[0]
        yrly_pct_change06.append(pct_change)
    SP500_changes06 = []
    for stock in yrly_pct_change06:
        yr_return = stock[-1] - stock[0]
        SP500_changes06.append(yr_return)

    ###: TEST FOR 'AMG' - yhoo finance: 2006 return was 1.1389
    # AMG = yrly_pct_change[5]
    # print(np.amax(AMG)) # 1.1390

    ###: GET RID OF NANs
    stocks_for_dict=[]
    for stock in stocks:
        stocks_for_dict.append(stock)
    stock_dict = dict(zip(stocks_for_dict, SP500_changes06))
    cleaned_dict = {val: stock_dict[val] for val in stock_dict if not isnan(stock_dict[val])}

    ###: COMPARE TO INVESTIGATE AND CHANGE ALLOC
    new_list=[]
    for stock, pctchange in cleaned_dict.items():
        new_list.append(stock)
    for x in stocks_for_dict:
        if x not in new_list:
            print("Deleting {}".format(x))
            ###: **DFS went public 2007**
    each_alloc_2006 = 1 / len(new_list)
    alloc_2006 = np.full((1, len(new_list)), each_alloc_2006)
    SP500_changes06_clean = []
    for key, val in cleaned_dict.items():
        SP500_changes06_clean.append(val)

    ### PORTFOLIO VALUE 2006 (even allocations)
    portval_2006 = np.dot(alloc_2006, SP500_changes06_clean)
    
    return portval_2006, df_2006

def find_daily_returns():
    portval_2006, df_2006 = annualized_returns()

    ### DAILY PERCENTAGE CHANGE
    daily_val_2006 = df_2006.copy()
    rets_daily_2006 = pd.DataFrame()
    for i in daily_val_2006:
        dlrets = (daily_val_2006[i].div(daily_val_2006[i].shift())) - 1
        dlrets = pd.DataFrame(dlrets)
        if rets_daily_2006.empty:
            rets_daily_2006 = dlrets
        else:
            rets_daily_2006 = rets_daily_2006.join(dlrets)
    return rets_daily_2006

def metrics():
    rets_daily_2006 = find_daily_returns()
    # we can't divide by t-1 on t = 1, so remove NaN
    rets_daily_2006 = rets_daily_2006[1:]
    rets_daily_2006.dropna(axis=1, inplace=True)
    mean_list_2006 = []
    vol_list_2006 = []
    for i in rets_daily_2006:
        means = np.mean(rets_daily_2006[i])
        mean_list_2006.append(means)
        vol = np.std(rets_daily_2006[i])
        vol_list_2006.append(vol)
    cleaned_avg_dly_ret_2006 = [x for x in mean_list_2006 if str(x) != 'nan']
    average_daily_return_2006 = round(np.mean(cleaned_avg_dly_ret_2006)*100,3)
    average_daily_volatility_2006 = round(np.mean(vol_list_2006),3)
    sharpe_2006 = round((average_daily_return_2006 - 0.02)/average_daily_volatility_2006,2)

    return average_daily_return_2006, average_daily_volatility_2006, sharpe_2006
