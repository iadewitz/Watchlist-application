# Download data from yahoo finance or pull them from a proper website
import yfinance as yf
import requests
import pandas as pd
import re

# Debug
ticker = "ENEL.MI";
start = "2023-10-10";
end = "2024-02-10";

def getValueByTicker(start = None, end = None):
    '''
    Wrapper function to download data
    Priority: 1. Yahoo Finance 2. 
    '''

def getValueByTickerYf(ticker, start = None, end = None):
    '''
    
    '''
    stock = yf.Ticker(ticker);
    stockInfo = stock.history(start = start, end = end)
    out = pd.DataFrame([stockInfo.index.strftime('%Y-%m-%d'), stockInfo['Close']]).T
    out["Currency"] = stock.info["currency"];
    out['Ticker'] = ticker
    out['Name'] = stock.info['shortName']
    out['Exchange'] = stock.info['exchange'];

    # Get time-zone value
    stockInfo = stockInfo.reset_index();
    timeZone = stockInfo['Date'].astype(str).str[-6:];   

    # Concat with out
    out = pd.concat([out, timeZone], axis = 1);
    out.columns = ['Date', 'Close_' + ticker, 'Currency', 'Ticker', 'Name', 'Exchange', 'TMZ']


    if not out.empty:
        return out
    else:
        return None
    

