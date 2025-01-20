import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import datetime
from src.utils.download_data import *
from src.utils.excel_generator import *

# Global variables definition
currentData = None;

def updateTable(tree, data):
    # Delete existing data
    for i in tree.get_children():
        tree.delete(i)

    # Set up columns
    tree["columns"] = list(data.columns)
    tree["show"] = "headings"

    # Fill the data
    dataRows = data.to_numpy().tolist()
    for row in dataRows:
        tree.insert("", "end", values = row)
    
    for column in tree["columns"]:
        tree.heading(column, text = column)


def onLoadData(tree):
    global currentData # The `global` keyword in Python is used to declare that a variable inside a function or block of code refers to a global variable,
    # which is a variable that is defined outside of the function or block.

    # Select last available file and read it
    lastFilePath = filedialog.askopenfilename()
    currentData = pd.read_excel(lastFilePath)

    # Create key
    currentData.reset_index();
    key = list();
    for j in range(0, currentData.shape[0]):
        elements = [currentData.loc[j, "Ticker"], 
                    currentData.loc[j, "PurchaseDate"], 
                    str(currentData.loc[j, "PurchasePrice"]), 
                    str(currentData.loc[j, "Quantity"])];
        key.append("_".join(elements));
    keysDataFrame = pd.DataFrame(key, columns = ["key"]);
    currentData = pd.concat([keysDataFrame, currentData], axis = 1);

    # Set new indices
    currentData.set_index("key", inplace = True);

    # Update table
    updateTable(tree, currentData);
    messagebox.showinfo("Info", "Last data loaded successfully");

def getCurrentData():
    global currentData;
    return currentData;

def onDownloadData(tree, startData, nDays):
    '''
    Download new data starting from current data 
    '''
    global currentData;

    # # Debug
    # tree = tree;
    # startData = currentData;
    # nDays = 30;

    # Get lastRunDate next date
    lastRunDate = startData.columns[-1] 
    lastRunDate = datetime.datetime.strptime(lastRunDate, '%Y-%m-%d') # Cast string to datetime 
    startDate = lastRunDate + datetime.timedelta(days = 1)
    startDate = startDate.strftime('%Y-%m-%d')
    endDate = datetime.datetime.today().strftime('%Y-%m-%d')

    uniqueTicker = list(set(startData["Ticker"])) # Get unique tickers for speeding up download
    stockValue = dict()
    for item in uniqueTicker:
        stockValue[item] = get_value_by_ticker_yf(item, start = startDate, end = endDate)

    # Dataframe with downloaded data
    outDataFrame = pd.DataFrame();
    for item in stockValue.keys() :
        if outDataFrame.empty:
            outDataFrame = stockValue[item];
        else:
            outDataFrame = pd.merge(outDataFrame, stockValue[item], on = "Date", how = "outer", suffixes = ('', f'_{item}'));

    outDataFrame.columns

    keys = list()
    for j in startData.index:
        elements = [startData.loc[j, "Ticker"], 
                    startData.loc[j, "PurchaseDate"], 
                    str(startData.loc[j, "PurchasePrice"]), 
                    str(startData.loc[j, "Quantity"])]
        keys.append("_".join(elements))

    # Retrieve information to create the key for the new data

    # Purchase date
    purchaseDate = dict()
    for j in startData.index:
        purchaseDate[j] = startData.loc[j, "PurchaseDate"]

    # Purchase price
    purchasePrice = dict()
    for j in startData.index:
        purchasePrice[j] = startData.loc[j, "PurchasePrice"]

    # Quantity
    quantity = dict()
    for j in startData.index:
        quantity[j] = startData.loc[j, "Quantity"]

    res = pd.DataFrame(index = startData.index)
    for key in res.index:
        ticker = str.split(key, sep = "_")[0]
        i = 0
        for date in outDataFrame["Date"]:
            res.loc[key, date] = outDataFrame.loc[i, "Close_" + ticker]
            i += 1
    
    # Merge on indices
    newData = pd.merge(currentData, res, left_index = True, right_index = True, how = 'outer');

    # Fill NaN
    newData = newData.ffill(axis = 1) # Forward fill: propagate the last known value (from left to right)
    # to the right (axis = 1) or below (axis = 0)

    # Round to 2 decimals
    for j in range(3, newData.shape[1]):
        newData.iloc[:, j] = newData.iloc[:, j].astype(float).round(2);
    
    # Truncate to last 30 days of data
    newData = pd.concat([newData.loc[:, ['Ticker', 'CompanyName', 'PurchaseDate', 'PurchasePrice', 'Quantity']],
                                 newData.iloc[:, range(-nDays, 0)]],
                                 axis = 1)
    
    # Current data always contains the current view in the tree
    currentData = newData;
    
    updateTable(tree, currentData)
    messagebox.showinfo("Info", "New data downloaded successfully")

def onAddData(tree, startData, newRow):

    # Get startData relevant dates
    lastDate = startData.columns[-1] 
    startDate = startData.columns[4] # The first date is always the 5th column 

    stockValue = dict()
    stockValue[ticker] = get_value_by_ticker_yf(ticker, start = startDate, end = lastDate)

def onSaveData(dataFrame):
    filePath = filedialog.askdirectory();
    generateExcel(dataFrame, filePath);
    messagebox.showinfo("Info", "Data saved successfully @ " + filePath + " folder");




