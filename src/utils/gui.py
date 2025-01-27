import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import datetime
from src.utils.download_data import *
from src.utils.excel_generator import *
import re

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

def updateTotal(tree, data, newRow, currency):
    # Add as the last row the total per day
    datePattern = re.compile(r'^\d{4}-\d{2}-\d{2}$');
        
    # Find indices of columns that match the date pattern
    notDatesIndices = [i for i, col in enumerate(data.columns) if not datePattern.match(col)];

    totalRow = ["Total (" + currency + ")"] + [""] * (len(notDatesIndices) - 1) + newRow;
    tree.insert("", "end", values = totalRow, tags = ("total", ))

    # Apply bold font to the total row
    tree.tag_configure("total", font = ("Helvetica", 10, "bold"))


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

def onDownloadData(tree, startData, nDays, startDate, endDate):
    '''
    Download new data starting from current data 
    '''
    global currentData;

    # Get relevant dates
    if nDays != '':
        endDate = datetime.datetime.today().strftime('%Y-%m-%d')
        startDate = datetime.datetime.strptime(endDate, '%Y-%m-%d') - datetime.timedelta(days = nDays)
        startDate = startDate.strftime('%Y-%m-%d')
    else:
        startDate = startDate;
        endDate = endDate;
    uniqueTicker = list(set(startData["Ticker"])) # Get unique tickers for speeding up download
    isNaN = True;
    while isNaN:
        stockValue = dict()
        for item in uniqueTicker:
            stockValue[item] = getValueByTickerYf(item, start = startDate, end = endDate)

        # Dataframe with downloaded data
        outDataFrame = pd.DataFrame();
        for item in stockValue.keys() :
            if outDataFrame.empty:
                outDataFrame = stockValue[item];
            else:
                outDataFrame = pd.merge(outDataFrame, stockValue[item], on = "Date", how = "outer", suffixes = ('', f'_{item}'));

        res = pd.DataFrame(index = startData.index)
        for key in res.index:
            ticker = str.split(key, sep = "_")[0]
            i = 0
            for date in outDataFrame["Date"]:
                res.loc[key, date] = outDataFrame.loc[i, "Close_" + ticker]
                i += 1
        
        if sum(res.iloc[:, 0].isna()) == 0:
            isNaN = False;
        else: 
            startDate = (datetime.datetime.strptime(startDate, '%Y-%m-%d') - datetime.timedelta(days = 1)).strftime('%Y-%m-%d');
    
    # Fill NaN
    res = res.ffill(axis = 1) # Forward fill: propagate the last known value (from left to right)
    # to the right (axis = 1) or below (axis = 0)

    # Merge on indices
    # Define the regular expression pattern for YYYY-MM-DD
    datePattern = re.compile(r'^\d{4}-\d{2}-\d{2}$');
        
    # Find indices of columns that match the date pattern
    notDatesIndices = [i for i, col in enumerate(startData.columns) if not datePattern.match(col)];
    newData = pd.merge(startData.iloc[:, notDatesIndices], res, left_index = True, right_index = True, how = 'outer');

    # Round to 2 decimals
    # Define the regular expression pattern for YYYY-MM-DD
    datePattern = re.compile(r'^\d{4}-\d{2}-\d{2}$');
        
    # Find indices of columns that match the date pattern
    floatIndices = [i for i, col in enumerate(newData.columns) if datePattern.match(col)];

    for j in floatIndices:
        newData.iloc[:, j] = newData.iloc[:, j].astype(float).round(2);
    
    # # Truncate to last nDays days of data
    # newData = pd.concat([newData.loc[:, ['Ticker', 'CompanyName', 'PurchaseDate', 'PurchasePrice', 'Quantity']],
    #                              newData.iloc[:, range(-nDays, 0)]],
    #                              axis = 1)
    
    # Current data always contains the current view in the tree
    currentData = newData;
    
    updateTable(tree, currentData)
    messagebox.showinfo("Info", "New data downloaded successfully")

def onAddData(tree, startData, newRow, startDate, endDate):
    global currentData;

    # Get startData relevant dates
    if currentData is None:
        startDate = startDate;
        endDate = endDate;

        # Dataframe with downloaded data
        outDataFrame = getValueByTickerYf(newRow.loc[0, "Ticker"], start = startDate, end = endDate);
    
        # Create the key for the new row
        elements = [newRow.loc[0, "Ticker"], 
                        newRow.loc[0, "PurchaseDate"], 
                        str(newRow.loc[0, "PurchasePrice"]), 
                        str(newRow.loc[0, "Quantity"])];
        key = "_".join(elements);
    
        # Create the row that will be concatanated to currentData
        res = pd.DataFrame(index = [key])
        res.loc[key, "Ticker"] = newRow.loc[0, "Ticker"];
        res.loc[key, "CompanyName"] = outDataFrame.loc[0, "Name"];
        res.loc[key, "PurchaseDate"] = newRow.loc[0, "PurchaseDate"];
        res.loc[key, "PurchasePrice"] = newRow.loc[0, "PurchasePrice"];
        res.loc[key, "Quantity"] = newRow.loc[0, "Quantity"];
        res.loc[key, "Currency"] = ", ".join(outDataFrame["Currency"].unique());
    
        # Now fill in the prices
        for date in outDataFrame["Date"]:
            index = outDataFrame.index[date == outDataFrame["Date"]];
            res.loc[key, date] = outDataFrame.loc[index, "Close_" + newRow.loc[0, "Ticker"]].values[0];

        # Uniformity
        newData = res;

        # Round to 2 decimals
        # Define the regular expression pattern for YYYY-MM-DD
        datePattern = re.compile(r'^\d{4}-\d{2}-\d{2}$');
    
        # Find indices of columns that match the date pattern
        floatIndices = [i for i, col in enumerate(newData.columns) if col == "Quantity" or datePattern.match(col)];

        for j in floatIndices:
            newData.iloc[:, j] = newData.iloc[:, j].astype(float).round(2);
        
        # Current data always contains the current view in the tree
        currentData = newData;
        
        updateTable(tree, currentData);
    else:
        # Find first and last dates
        datePattern = re.compile(r'^\d{4}-\d{2}-\d{2}$');

        # Find indices of columns that match the date pattern
        dateIndices = [i for i, col in enumerate(startData.columns) if datePattern.match(col)];
        endDate = startData.columns[dateIndices[-1]];
        startDate = startData.columns[dateIndices[0]]; 
        
        # Dataframe with downloaded data
        outDataFrame = getValueByTickerYf(newRow.loc[0, "Ticker"], start = startDate, end = endDate);        

        # Create the key for the new row
        elements = [newRow.loc[0, "Ticker"], 
                    newRow.loc[0, "PurchaseDate"], 
                    str(newRow.loc[0, "PurchasePrice"]), 
                    str(newRow.loc[0, "Quantity"])];
        key = "_".join(elements);
        
        # Create the row that will be concatanated to currentData
        # Create ordered columns
        # Get unique dates
        uniqueDates = list(set(currentData.columns[dateIndices].tolist() + outDataFrame["Date"].tolist()));

        # Convert to datetime objects and sort
        uniqueDates = sorted([datetime.datetime.strptime(date, '%Y-%m-%d') for date in uniqueDates])

        # Convert back to strings
        uniqueDates = [date.strftime('%Y-%m-%d') for date in uniqueDates]

        newColumns = [col for i, col in enumerate(currentData.columns) if i not in dateIndices] + uniqueDates     
        res = pd.DataFrame(index = [key], columns = newColumns);
        res.loc[key, "Ticker"] = newRow.loc[0, "Ticker"];
        res.loc[key, "CompanyName"] = outDataFrame.loc[0, "Name"];
        res.loc[key, "PurchaseDate"] = newRow.loc[0, "PurchaseDate"];
        res.loc[key, "PurchasePrice"] = newRow.loc[0, "PurchasePrice"];
        res.loc[key, "Quantity"] = newRow.loc[0, "Quantity"];
        res.loc[key, "Currency"] = ", ".join(outDataFrame["Currency"].unique());

        # Now fill in the prices
        for date in outDataFrame["Date"]:
            index = outDataFrame.index[date == outDataFrame["Date"]];
            res.loc[key, date] = outDataFrame.loc[index, "Close_" + newRow.loc[0, "Ticker"]].values[0];

        # Concat on row
        newData = pd.DataFrame(index = list(currentData.index), columns = newColumns)
        for index in currentData.index:
            for col in currentData.columns:
                newData.at[index, col] = currentData.at[index, col];
        
        newData = pd.concat([newData, res], axis = 0)

        # Round to 2 decimals
        # Define the regular expression pattern for YYYY-MM-DD
        datePattern = re.compile(r'^\d{4}-\d{2}-\d{2}$');
        
        # Find indices of columns that match the date pattern
        floatIndices = [i for i, col in enumerate(newData.columns) if col == "Quantity" or datePattern.match(col)];

        for j in floatIndices:
            newData.iloc[:, j] = newData.iloc[:, j].astype(float).round(2);
        
        # Current data always contains the current view in the tree
        currentData = newData;
        
        updateTable(tree, currentData)
        messagebox.showinfo("Info", "New data downloaded successfully.\nRemember to refresh the data!")


def onSaveData(dataFrame):
    filePath = filedialog.askdirectory();
    generateExcel(dataFrame, filePath);
    messagebox.showinfo("Info", "Data saved successfully @ " + filePath + " folder");

def onComputeTotal(tree, data, currency):
    global currentData;

    # Get relevant dates
    datePattern = re.compile(r'^\d{4}-\d{2}-\d{2}$');
    dateIndices = [i for i, col in enumerate(data.columns) if datePattern.match(col)];

    endDate = datetime.datetime.strptime(data.columns[dateIndices[-1]], '%Y-%m-%d') + datetime.timedelta(days = 1);
    endDate = endDate.strftime('%Y-%m-%d');
    startDate = data.columns[dateIndices[0]];
    
    # Get relevant FX rates
    relevantFxRates = [];
    for cur in data["Currency"].unique():
        if cur != currency:
            relevantFxRates.append(cur + currency + "=X");
    fxRates = dict()
    for item in relevantFxRates:
        fxRates[item] = getValueByTickerYf(item, start = startDate, end = endDate); 

    # Create a dataframe with the relevant dates
    res = pd.DataFrame(index = fxRates.keys(), columns = data.columns[dateIndices]);
    for key in res.index:
            outDataFrame = fxRates[key]
            for date in res.columns:
                # Now fill in the prices
                index = outDataFrame.index[date == outDataFrame["Date"]];
                res.loc[key, date] = outDataFrame.loc[index, "Close_" + key].values[0];

    totalDataFrame = pd.DataFrame(index = data.index, columns = data.columns[dateIndices]);
    for index in totalDataFrame.index:
        tmpCurrency = data.loc[index, "Currency"];
        if tmpCurrency != currency:
            for col in totalDataFrame.columns:
                totalDataFrame.loc[index, col] = data.loc[index, "Quantity"] * data.loc[index, col] * res.loc[tmpCurrency + currency + "=X", col]
        else:
             for col in totalDataFrame.columns:
                totalDataFrame.loc[index, col] = data.loc[index, "Quantity"] * data.loc[index, col]
    
    totalPerDay = totalDataFrame.sum(axis = 0);

    # Round to 2 decimals
    totalPerDay = totalPerDay.astype(float).round(2);
    if sum(totalPerDay.index != data.columns[dateIndices]) == 0:
        totalPerDay = list(totalPerDay);
        updateTotal(tree, currentData, totalPerDay, currency);
    else:
        messagebox.showerror("Error", "Something went wrong.");
