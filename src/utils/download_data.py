# Download data from yahoo finance or pull them from a proper website
import yfinance as yf
import requests
import pandas as pd
import re

# # Debug
# ticker = "AAPL";
# start = "2023-10-10";
# end = "2024-02-10";

def get_value_by_ticker_yf(ticker, start = None, end = None):
    '''
    
    '''
    stock = yf.Ticker(ticker)
    stockInfo = stock.history(start = start, end = end)
    out = pd.DataFrame([stockInfo.index.strftime('%Y-%m-%d'), stockInfo['Close']]).T
    out["Currency"] = stock.info["currency"];
    out['Ticker'] = ticker
    out['Name'] = stock.info['shortName']
    out.columns = ['Date', 'Close_' + ticker, 'Currency', 'Ticker', 'Name']
    if not out.empty:
        return out
    else:
        return None