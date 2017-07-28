Working with cool tools like pickle, BeautifulSoup, and pandas_datareader for financial data!!

Using pickle to serialize Wikipedia table ( SP500 stock list - https://en.wikipedia.org/wiki/List_of_S%26P_500_companies )
Took all stocks on SP500 in 'Financials' sector and pulled Google historical data to dataframe of closing price and equity name with respective start-end dates as the index.

'porfolio_metrics.py' calculates following portfolio metrics of made-up bank index:

1) Average Daily Return
2) Average Daily Volatility
3) Sharpe Ratio
...

Assumptions of index exist in code documentation (see 'portfolio_metrics.py')
