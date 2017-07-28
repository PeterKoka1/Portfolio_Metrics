Working with cool tools like pickle, BeautifulSoup, and pandas_datareader for financial data!!

Using pickle to serialize Wikipedia table ( SP500 stock list - https://en.wikipedia.org/wiki/List_of_S%26P_500_companies )
Took all stocks on SP500 in 'Financials' sector and pulled Google historical data to dataframe of closing price and equity name with respective start-end dates as the index.

'porfolio_metrics.py' calculates following portfolio metrics of made-up bank index:

1) Yearly Portfolio Value % Change
2) Average Daily Return
3) Average Daily Volatility
4) Sharpe Ratio

Assumptions of index exist in code documentation (see 'portfolio_metrics.py')

FINAL RESULTS:

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
