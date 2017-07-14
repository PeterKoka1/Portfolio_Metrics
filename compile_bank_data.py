import datetime as dt
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import style
from pylab import *
import pandas_datareader.data as web
import requests
import bs4 as bs
import pickle
import sys
import os
from os.path import exists
import warnings
warnings.filterwarnings('ignore')

def bank_pull_test():
    stocks_interested = ['GS','MS','JPM','BAC']
    dt_start = dt.datetime(2006,5,5)
    dt_end = dt.datetime(2009,1,1)
    for i in stocks_interested:
        if not exists('{}.csv'.format(i)):
            df = web.DataReader(i,
                            'google',
                            dt_start,dt_end)
            df.to_csv('{}.csv'.format(i))
        else:
            print("{}.csv".format(i) + " already exists.")
    #goldman_current = web.get_data_yahoo('GS', dt.datetime.today())
    #print(goldman_current)
    return dt_start, dt_end, stocks_interested

def plot_test(dt_start, dt_end, stocks_interested):
    # print(plt.style.available)
    style.use('ggplot')

    for i in stocks_interested:
        df = pd.read_csv('{}.csv'.format(i),
                        parse_dates=True,
                        index_col=0)

        df['100ma'] = pd.Series((df['Close'].rolling(window=100, min_periods=0).mean()), index=df.index)
        df['10ma'] = pd.Series((df['Close'].rolling(window=10, min_periods=0).mean()), index=df.index)

        fig = gcf()
        axes1 = plt.subplot2grid((7,1),(0,0), rowspan=5, colspan=2)
        axes2 = plt.subplot2grid((7,1),(5,0), rowspan=5, colspan=0, sharex=axes1)

        axes1.get_xaxis().set_visible(False)
        axes1.plot(df.index, df['Close'])
        axes1.plot(df.index, df['100ma'])
        axes1.plot(df.index, df['10ma'])
        axes2.bar(df.index, df['Volume'], width=3, color='black')
        plt.xlim(dt_start, dt_end)
        fig.suptitle('{}'.format(i))

        plt.show()

def save_all_financials():
    r = requests.get('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies') # scanning HTML
    soup = bs.BeautifulSoup(r.text, 'lxml')
    SP500financials = soup.find('table', {'class':'wikitable sortable'})
    tickers = []
    sector = []

    for ticks in SP500financials.findAll('tr')[1:]: # tr 1 onward (we don't need titles)
        stock = ticks.findAll('td')[0].text # we want 1st column
        tickers.append(stock)
    # print(tickers)

    for sect in SP500financials.findAll('tr')[1:]:
        sectors = sect.findAll('td')[3].text
        sector.append(sectors)
    # print(sector)

    tickers = dict(zip(tickers, sector))
    df_ticks = []
    for key, value in tickers.items():
        if value == 'Financials':
            df_ticks.append(key)

    with open('SP500financials.pickle','wb') as f:
        pickle.dump(df_ticks,f)

def get_data(dt_start, dt_end, already_loaded=False):
    if already_loaded:
        df_ticks = save_all_financials()
    else:
        with open('SP500financials.pickle','rb') as f:
            df_ticks = pickle.load(f)

    if exists('financials_2006_2009'):
        print("File exists")
    else:
        os.makedirs('financials_2006_2009')

    for ticker in df_ticks:
        if not exists('financials_2006_2009/{}'.format(ticker)):
            each_stock = web.DataReader(ticker, 'google', dt_start, dt_end) ###: GETTING FINANCIAL DATA
            each_stock.to_csv('financials_2006_2009/{}'.format(ticker))
        else:
            print("Stock in directory")

def combine_data():
    with open('SP500financials.pickle', 'rb') as f:
        df_ticks = pickle.load(f)

    df = pd.DataFrame()

    for ticker in df_ticks:
        df_ = pd.read_csv('financials2006_2009/{}'.format(ticker)).set_index('Date')
        df_.drop(['Open', 'High', 'Low', 'Volume'], axis=1, inplace=True)
        df_.rename(columns={'Close':ticker}, inplace=True)
        df_ = pd.DataFrame(df_)

        if ticker not in df:
            df = df.join(df_, how='outer') # 'outer' will preserve alphabetical order
        else:
            print(ticker, " already in dataframe.")

    df.to_csv('SP500_financials2006-2009')

def main():
    dt_start, dt_end, stocks_interested = bank_pull_test()
    #bank_pull_test()
    #plot_test(dt_start, dt_end, stocks_interested)
    save_all_financials()
    get_data(dt_start,dt_end)
    combine_data()

if __name__ == '__main__':
    main()
