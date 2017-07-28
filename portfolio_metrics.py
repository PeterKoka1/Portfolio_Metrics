"""
Assumptions of 'financial index':
1) even weighting distribution of each equity in portfolio
2) equities were held from dt_start ('2006-05-06') to dt_end ('2008-12-31')
3) all calculations are based on those time periods
"""

import pandas as pd
import numpy as np
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

    ###: manual date checks
    df_2006 = df[df['Date'] < '2007-01-01']
    df_2007 = df[166:417]
    df_2008 = df[417:671]

    return df_2006, df_2007, df_2008

def annualized_returns():

    df_2006, df_2007, df_2008 = set_years()
    each_alloc = 1 / len(stocks)
    alloc = np.full((1, len(stocks)), each_alloc)

    ###: 2006 returns
    df_2006.set_index('Date', inplace=True)
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

    ###: 2007 returns
    df_2007.set_index('Date', inplace=True)
    df_2007.fillna(0, inplace=True)
    yrly_pct_change07 = []
    for stock in df_2007:
        vals = df_2007[stock].values.copy()
        pct_change = vals / vals[0]
        yrly_pct_change07.append(pct_change)

    SP500_changes07 = []
    for stock in yrly_pct_change07:
        yr_return = stock[-1] - stock[0]
        SP500_changes07.append(yr_return)

    ###: GET RID OF NANs
    stocks_for_dict = []
    for stock in stocks:
        stocks_for_dict.append(stock)
    stock_dict = dict(zip(stocks_for_dict, SP500_changes07))
    cleaned_dict = {val: stock_dict[val] for val in stock_dict if not isnan(stock_dict[val])}

    ###: COMPARE TO INVESTIGATE AND CHANGE ALLOC
    new_list = []
    for stock, pctchange in cleaned_dict.items():
        new_list.append(stock)
    for x in stocks_for_dict:
        if x not in new_list:
            print("Deleting {}".format(x))
    each_alloc_2007 = 1 / len(new_list)
    alloc_2007 = np.full((1, len(new_list)), each_alloc_2007)
    SP500_changes07_clean = []
    for key, val in cleaned_dict.items():
        SP500_changes07_clean.append(val)

    ### PORTFOLIO VALUE 2007 (even allocations)
    portval_2007 = np.dot(alloc_2007, SP500_changes07_clean)

    ###: 2008 returns
    df_2008.set_index('Date', inplace=True)
    df_2008.fillna(0, inplace=True)
    yrly_pct_change08 = []
    for stock in df_2008:
        vals = df_2008[stock].values.copy()
        pct_change = vals / vals[0]
        yrly_pct_change08.append(pct_change)

    SP500_changes08 = []
    for stock in yrly_pct_change08:
        yr_return = stock[-1] - stock[0]
        SP500_changes08.append(yr_return)

    ###: GET RID OF NANs
    stocks_for_dict = []
    for stock in stocks:
        stocks_for_dict.append(stock)
    stock_dict = dict(zip(stocks_for_dict, SP500_changes08))
    cleaned_dict = {val: stock_dict[val] for val in stock_dict if not isnan(stock_dict[val])}

    ###: COMPARE TO INVESTIGATE AND CHANGE ALLOC
    new_list = []
    for stock, pctchange in cleaned_dict.items():
        new_list.append(stock)
    for x in stocks_for_dict:
        if x not in new_list:
            print("Deleting {}".format(x))
    each_alloc_2008 = 1 / len(new_list)
    alloc_2008 = np.full((1, len(new_list)), each_alloc_2008)
    SP500_changes08_clean = []
    for key, val in cleaned_dict.items():
        SP500_changes08_clean.append(val)

    ### PORTFOLIO VALUE 2008 (even allocations)
    portval_2008 = np.dot(alloc_2008, SP500_changes08_clean)

    return portval_2006, df_2006, portval_2007, df_2007, portval_2008, df_2008

def find_daily_returns():

    portval_2006, df_2006, portval_2007, df_2007, portval_2008, df_2008 = annualized_returns()

    ###: DAILY PERCENTAGE CHANGE 2006
    daily_val_2006 = df_2006.copy()
    rets_daily_2006 = pd.DataFrame()

    for i in daily_val_2006:

        dlrets = (daily_val_2006[i].div(daily_val_2006[i].shift())) - 1

        dlrets = pd.DataFrame(dlrets)
        if rets_daily_2006.empty:
            rets_daily_2006 = dlrets
        else:
            rets_daily_2006 = rets_daily_2006.join(dlrets)

    ###: DAILY PERCENTAGE CHANGE 2007
    daily_val_2007 = df_2007.copy()
    rets_daily_2007 = pd.DataFrame()

    for i in daily_val_2007:

        dlrets = (daily_val_2007[i].div(daily_val_2007[i].shift())) - 1

        dlrets = pd.DataFrame(dlrets)
        if rets_daily_2007.empty:
            rets_daily_2007 = dlrets
        else:
            rets_daily_2007 = rets_daily_2007.join(dlrets)

    ###: DAILY PERCENTAGE CHANGE 2008
    daily_val_2008 = df_2008.copy()
    rets_daily_2008 = pd.DataFrame()

    for i in daily_val_2008:

        dlrets = (daily_val_2008[i].div(daily_val_2008[i].shift())) - 1

        dlrets = pd.DataFrame(dlrets)
        if rets_daily_2008.empty:
            rets_daily_2008 = dlrets
        else:
            rets_daily_2008 = rets_daily_2008.join(dlrets)


    return rets_daily_2006, rets_daily_2007, rets_daily_2008, portval_2006, portval_2007, portval_2008

find_daily_returns()

def metrics():

    rets_daily_2006, rets_daily_2007, rets_daily_2008, portval_2006, portval_2007, portval_2008 = find_daily_returns()

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
    portval_2006 = round(portval_2006.item()*100,3)
    print("Portval Change 2006: {}%".format(portval_2006))
    print("2006 Average Daily Return: {}%".format(average_daily_return_2006))
    print("2006 Average Daily Volatility {}%".format(average_daily_volatility_2006))
    print("2006 Sharpe Ratio: {}".format(sharpe_2006))

    rets_daily_2007 = rets_daily_2007[1:]
    rets_daily_2007.dropna(axis=1, inplace=True)
    mean_list_2007 = []
    vol_list_2007 = []
    for i in rets_daily_2007:
        means = np.mean(rets_daily_2007[i])
        mean_list_2007.append(means)
        vol = np.std(rets_daily_2007[i])
        vol_list_2007.append(vol)
    cleaned_avg_dly_ret_2007 = [x for x in mean_list_2007 if str(x) != 'nan']
    average_daily_return_2007 = round(np.mean(cleaned_avg_dly_ret_2007) * 100, 3)
    average_daily_volatility_2007 = round(np.mean(vol_list_2007), 3)
    sharpe_2007 = round((average_daily_return_2007 - 0.02) / average_daily_volatility_2007, 2)
    portval_2007 = round(portval_2007.item()*100, 3)
    print("Portval Change 2007: {}%".format(portval_2007))
    print("2007 Average Daily Return: {}%".format(average_daily_return_2007))
    print("2007 Average Daily Volatility {}%".format(average_daily_volatility_2007))
    print("2007 Sharpe Ratio: {}".format(sharpe_2007))

    rets_daily_2008 = rets_daily_2008[1:]
    rets_daily_2008.dropna(axis=1, inplace=True)
    mean_list_2008 = []
    vol_list_2008 = []
    for i in rets_daily_2008:
        means = np.mean(rets_daily_2008[i])
        mean_list_2008.append(means)
        vol = np.std(rets_daily_2008[i])
        vol_list_2008.append(vol)
    cleaned_avg_dly_ret_2008 = [x for x in mean_list_2008 if str(x) != 'nan']
    average_daily_return_2008 = round(np.mean(cleaned_avg_dly_ret_2008) * 100, 3)
    average_daily_volatility_2008 = round(np.mean(vol_list_2008), 3)
    sharpe_2008 = round((average_daily_return_2008 - 0.02) / average_daily_volatility_2008, 2)
    portval_2008 = round(portval_2008.item()*100, 3)
    print("Portval Change 2008: {}%".format(portval_2008))
    print("2008 Average Daily Return: {}%".format(average_daily_return_2008))
    print("2008 Average Daily Volatility {}%".format(average_daily_volatility_2008))
    print("2008 Sharpe Ratio: {}".format(sharpe_2008))

def main():
    metrics()
    
if __name__ == '__main__':
    main()

"""
Portval Change 2006: +5.793%
2006 Average Daily Return: 0.04%
2006 Average Daily Volatility 0.013%
2006 Sharpe Ratio: 1.54

Portval Change 2007: -2.938%
2007 Average Daily Return: -0.028%
2007 Average Daily Volatility 0.018%
2007 Sharpe Ratio: -2.67

Portval Change 2008: -39.606%
2008 Average Daily Return: -0.099%
2008 Average Daily Volatility 0.053%
2008 Sharpe Ratio: -2.25

"""
