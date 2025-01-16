# Download data from yahoo finance or pull them from a proper website
import yfinance as yf
import requests
import pandas as pd

def get_value_by_ticker_yf(ticker, start = None, end = None):
    '''
    
    '''
    stock = yf.Ticker(ticker)
    stockInfo = stock.history(start = start, end = end)
    out = pd.DataFrame([stockInfo.index.strftime('%Y-%m-%d'), stockInfo['Close']]).T
    out['Ticker'] = ticker
    name = stock.info['shortName']
    out['Name'] = name
    out.columns = ['Date', 'Close_' + ticker, 'Ticker', 'Name']
    if not out.empty:
        return out
    else:
        return None
    