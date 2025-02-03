import datetime
import pandas as pd
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import sys

# Import custom modules
from src.utils import gui

def onLoadDataEvent(tree):
    global currentData;
    gui.onLoadData(tree);
    currentData = gui.getCurrentData(); # loadButton change the value of currentData
    print(f"currentData updated: {currentData.head()}");

def onDownloadDataEvent(tree, data):
    def submitDays():
        global currentData; # The declaration of a variable as global must be contained where the assignment lives; otherwise, a new local variabale would be created
        nDays = '';
        startDate = '';
        endDate = '';
        if nDaysEntry.get() != '':
            nDays = int(nDaysEntry.get());
        else:
            startDate = startDateEntry.get();
            endDate = endDateEntry.get();
        gui.onDownloadData(tree, data, nDays, startDate, endDate);
        currentData = gui.getCurrentData(); # downloadButton change the value of currentData
        print(f"currentData updated: {currentData.head()}");
        selectDataWindow.destroy();

    # Create the window to select the number of days to display and record
    selectDataWindow = tk.Toplevel();
    selectDataWindow.title("Select the number of days to display");
    selectDataWindow.geometry("600x450");

    tk.Label(selectDataWindow, text = "Last number of days:").pack(pady = 5);
    nDaysEntry = tk.Entry(selectDataWindow);
    nDaysEntry.pack(pady = 5);

    tk.Label(selectDataWindow, text = "Start Date (YYYY-MM-DD):").pack(pady = 5);
    startDateEntry = tk.Entry(selectDataWindow);
    startDateEntry.pack(pady = 5);

    tk.Label(selectDataWindow, text = "End Date (YYYY-MM-DD):").pack(pady = 5);
    endDateEntry = tk.Entry(selectDataWindow);
    endDateEntry.pack(pady = 5);

    submitButton = tk.Button(selectDataWindow, text = "Submit", command = submitDays);
    submitButton.pack(pady = 10);

def onAddDataEvent(tree, startData):
    global currentData;

    def submitData():
        global currentData;
        startDate = None;
        endDate = None;

        ticker = tickerEntry.get();
        purchasePrice = float(priceEntry.get());
        purchaseDate = dateEntry.get();
        quantity = float(quantityEntry.get());
        if currentData is None:
            startDate = startDateEntry.get();
            endDate = endDateEntry.get();

        # Process the data (e.g., add to currentData)
        newRow = pd.DataFrame([[ticker, purchasePrice, purchaseDate, quantity]], columns = ["Ticker", "PurchasePrice", "PurchaseDate", "Quantity"]);
        gui.onAddData(tree, currentData, newRow, startDate, endDate);
        currentData = gui.getCurrentData(); 
        # print(f"currentData updated: {currentData.head()}");
        addWindow.destroy();

    # Two possible entries: if no data has been uploaded -> insert also the start and end dates; otherwise take them from currentData 
    if currentData is None:
        # If currentData is empty, then we are at its inizialization 
        addWindow = tk.Toplevel();
        addWindow.title("Add new data");
        addWindow.geometry("600x450");

        tk.Label(addWindow, text = "Ticker:").pack(pady = 5);
        tickerEntry = tk.Entry(addWindow);
        tickerEntry.pack(pady = 5);

        tk.Label(addWindow, text = "Purchase Price (use . as decimal separator):").pack(pady = 5);
        priceEntry = tk.Entry(addWindow);
        priceEntry.pack(pady = 5);

        tk.Label(addWindow, text = "Purchase Date (YYYY-MM-DD):").pack(pady = 5);
        dateEntry = tk.Entry(addWindow);
        dateEntry.pack(pady=5);

        tk.Label(addWindow, text = "Quantity (use . as decimal separator):").pack(pady = 5);
        quantityEntry = tk.Entry(addWindow);
        quantityEntry.pack(pady=5);

        tk.Label(addWindow, text = "Start Date (YYYY-MM-DD):").pack(pady = 5);
        startDateEntry = tk.Entry(addWindow);
        startDateEntry.pack(pady = 5);

        tk.Label(addWindow, text = "End Date (YYYY-MM-DD):").pack(pady = 5);
        endDateEntry = tk.Entry(addWindow);
        endDateEntry.pack(pady = 5);

        submitButton = tk.Button(addWindow, text = "Submit", command = submitData);
        submitButton.pack(pady = 10);
    else:
        # If currentData is not empty -> the new data will follow its time window
        addWindow = tk.Toplevel();
        addWindow.title("Add new data");
        addWindow.geometry("600x450");

        tk.Label(addWindow, text = "Ticker:").pack(pady = 5);
        tickerEntry = tk.Entry(addWindow);
        tickerEntry.pack(pady = 5);

        tk.Label(addWindow, text = "Purchase Price (use . as decimal separator):").pack(pady = 5);
        priceEntry = tk.Entry(addWindow);
        priceEntry.pack(pady = 5);

        tk.Label(addWindow, text = "Purchase Date (YYYY-MM-DD):").pack(pady = 5);
        dateEntry = tk.Entry(addWindow);
        dateEntry.pack(pady=5);

        tk.Label(addWindow, text = "Quantity (use . as decimal separator):").pack(pady = 5);
        quantityEntry = tk.Entry(addWindow);
        quantityEntry.pack(pady=5);

        submitButton = tk.Button(addWindow, text = "Submit", command = submitData);
        submitButton.pack(pady = 10);

def onComputeTotalEvent(tree, currentData):
    def computeTotal():
        global currentData;

        currency = currencyEntry.get();
        if currentData is None or currentData.empty:
            messagebox.showerror("Error", "There are no loaded data!");
        else:
            gui.onComputeTotal(tree, currentData, currency);
        computeTotalWindow.destroy();

    computeTotalWindow = tk.Toplevel();
    computeTotalWindow.title("Compute total");
    computeTotalWindow.geometry("600x450");

    tk.Label(computeTotalWindow, text = "Currency:").pack(pady = 5);
    currencyEntry = tk.Entry(computeTotalWindow);
    currencyEntry.pack(pady = 5);

    submitButton = tk.Button(computeTotalWindow, text = "Submit", command = computeTotal);
    submitButton.pack(pady = 10);

def onPlot(data):

    def onPlotButton():
        selectedKeys = [listBox.get(i) for i in listBox.curselection()];
        gui.plotKeys(data, selectedKeys);

    plotWindow = tk.Toplevel();
    plotWindow.title("Plot series");
    plotWindow.geometry("600x450");

    tk.Label(plotWindow, text = "Select Ticker:").pack(pady = 5);

    # Create a listbox
    listBox = tk.Listbox(plotWindow, selectmode = tk.MULTIPLE);
    listBox.pack(fill = tk.BOTH, expand = True, pady = 5);

    # Add tickers to the listbox
    keys = data.index;
    for key in keys:
        listBox.insert(tk.END, key);

    plotButton = tk.Button(plotWindow, text = "Plot", command = onPlotButton);
    plotButton.pack(pady = 10);

def onShowPrices(tree, data):
    gui.updateTable(tree, currentData);

def onShowReturns(tree, data):
    gui.updateReturns(tree, data);

def main():
    # GUI setup
    root = tk.Tk() # Create a widget/frame
    root.title("Stock Data Manager")
    root.geometry("800x600")  # Set a fixed size for the root window

    # Create a frame for the table and scrollbars
    tableFrame = tk.Frame(root)
    tableFrame.pack(fill = tk.BOTH, expand = True)

    # Create Treeview
    tree = ttk.Treeview(tableFrame)
    tree.pack(side = tk.LEFT, fill = tk.BOTH, expand = True)

    # Add vertical scrollbar to the Treeview
    vsb = ttk.Scrollbar(tree, orient = "vertical", command = tree.yview)
    vsb.pack(side = tk.RIGHT, fill = tk.Y)

    # Add horizontal scrollbar to the Treeview
    hsb = ttk.Scrollbar(tree, orient = "horizontal", command = tree.xview)
    hsb.pack(side = tk.BOTTOM, fill = tk.X)

    tree.configure(yscrollcommand = vsb.set, xscrollcommand = hsb.set)
    
    # Download button
    downloadDataButton = tk.Button(root, text = "Download New Data", command = lambda: onDownloadDataEvent(tree, currentData)) # The command parameter of a button is called immediately after
    # its creation if the function is called directly instead of passing a reference to it. The lambda function is used to pass a reference of the function 
    downloadDataButton.pack(pady = 10)

    # Add data button
    addDataButton = tk.Button(root, text = "Add New Data", command = lambda: onAddDataEvent(tree, currentData))
    addDataButton.pack(pady = 10)

    # Create a menu bar
    menuBar = tk.Menu(root)
    root.config(menu = menuBar)

    # Create a File menu
    fileMenu = tk.Menu(menuBar, tearoff = 0)
    menuBar.add_cascade(label = "File", menu = fileMenu)
    fileMenu.add_command(label = "Load Data", command = lambda: onLoadDataEvent(tree))
    fileMenu.add_command(label = "Save Current View", command = lambda: gui.onSaveData(currentData))
    fileMenu.add_separator()
    fileMenu.add_command(label = "Exit", command = root.destroy)

    # Create an Compute menu
    computeMenu = tk.Menu(menuBar, tearoff = 0)
    menuBar.add_cascade(label = "Compute", menu = computeMenu)
    computeMenu.add_command(label = "Compute Total", command = lambda: onComputeTotalEvent(tree, currentData))
    computeMenu.add_separator()
    # computeMenu.add_command(label = "Compute Risk Metrics", command = lambda: onComputeTotalEvent(tree, currentData))


    # Create a View menu
    viewMenu = tk.Menu(menuBar, tearoff = 0)
    menuBar.add_cascade(label = "View", menu = viewMenu)
    viewMenu.add_command(label = "Prices", command = lambda: onShowPrices(tree, currentData));
    viewMenu.add_command(label = "Returns", command = lambda: onShowReturns(tree, currentData));
    viewMenu.add_separator()
    viewMenu.add_command(label = "Plot", command = lambda: onPlot(currentData));

    # Create a Help menu
    helpMenu = tk.Menu(menuBar, tearoff = 0)
    menuBar.add_cascade(label = "Help", menu = helpMenu)
    helpMenu.add_command(label = "About", command = lambda: messagebox.showinfo("About",
                                                                                "Stock Data Manager v1.0.\nVisit https://github.com/iadewitz/Watchlist-application."))

    # root.mainloop()

# Variables definiton
currentData = None;
currentReturns = None;
riskMetrics = None;

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"An error occurred: {e}")
        input("Press Enter to exit...")
