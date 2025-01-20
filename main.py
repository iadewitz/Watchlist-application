import datetime
import pandas as pd
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import sys

# Import custom modules
from src.utils import gui

# # Write Excel
# outFileName = 
# generate_excel(finalDataFrame, outFileName)

def onLoadDataEvent(tree):
    global currentData;
    gui.onLoadData(tree);
    currentData = gui.getCurrentData(); # loadButton change the value of currentData
    print(f"currentData updated: {currentData.head()}");

def onDownloadDataEvent(tree, data):
    def submitDays():
        global currentData; # The declaration of a variable as global must be contained where the assignment lives; otherwise, a new local variabale would be created
        nDays = int(nDaysEntry.get());
        gui.onDownloadData(tree, data, nDays);
        currentData = gui.getCurrentData(); # downloadButton change the value of currentData
        print(f"currentData updated: {currentData.head()}");
        selectDataWindow.destroy();

    # Create the window to select the number of days to display and record
    selectDataWindow = tk.Toplevel();
    selectDataWindow.title("Select the number of days to display");
    selectDataWindow.geometry("600x450");

    tk.Label(selectDataWindow, text = "Number of days:").pack(pady = 5);
    nDaysEntry = tk.Entry(selectDataWindow);
    nDaysEntry.pack(pady = 5);

    submitButton = tk.Button(selectDataWindow, text = "Submit", command = submitDays);
    submitButton.pack(pady = 10);

def onAddDataEvent(tree, startData):
    def submitData():
        global currentData;
        ticker = tickerEntry.get();
        purchasePrice = float(float(priceEntry.get()));
        purchaseDate = dateEntry.get();
        quantity = float(quantityEntry.get());

        # Debug:
        ticker = "MSFT";
        purchasePrice = 78.78;
        purchaseDate = "2023-10-23";
        quantity = 32;

        # Process the data (e.g., add to currentData)
        newRow = pd.DataFrame([[ticker, priceEntry, dateEntry, quantity]], columns = ["Ticker", "PurchasePrice", "PurchaseDate", "Quantity"]);
        currentData = pd.concat([currentData, newRow], ignore_index = True);
        gui.onAddData(tree, startData, newRow);
        currentData = gui.getCurrentData(); # downloadButton change the value of currentData
        print(f"currentData updated: {currentData.head()}");
        addWindow.destroy();

    # Create the window to add data
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
    vsb.pack(side = tk.LEFT, fill = tk.Y)

    # Add horizontal scrollbar to the Treeview
    hsb = ttk.Scrollbar(tree, orient = "horizontal", command = tree.xview)
    hsb.pack(side = tk.BOTTOM, fill = tk.X)

    tree.configure(yscrollcommand = vsb.set, xscrollcommand = hsb.set)

    loadButton = tk.Button(root, text = "Load Last Data", command = lambda: onLoadDataEvent(tree)) # The command parameter of a button is called immediately after its creation if the function is
    # called directly instead of passing a reference to it. The lambda function is used to pass a reference of the function 
    loadButton.pack(pady = 10)
    
    downloadDataButton = tk.Button(root, text = "Download New Data", command = lambda: onDownloadDataEvent(tree, currentData))
    downloadDataButton.pack(pady = 10)

    addDataButton = tk.Button(root, text = "Add New Data", command = lambda: onAddDataEvent(tree, currentData))
    addDataButton.pack(pady = 10)

    saveDataButton = tk.Button(root, text = "Save Current View", command = lambda: gui.onSaveData(currentData))
    saveDataButton.pack(pady = 10)
    
    # computeTotalRow = tk.Button(root, text = "Compute Total", command = lambda: onComputeTotalEvent(tree, currentData))
    # computeTotalRow.pack(pady = 10)

    # plotButton = tk.Button(root, text = "Plot Data", command = on_plot_data)
    # plotButton.pack(pady = 10)

    # computeVaRButton = tk.Button(root, text = "Plot Data", command = lambda: onComputeVaREvent(tree, currentData))
    # computeVaRButton.pack(pady = 10)

    root.mainloop()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"An error occurred: {e}")
        input("Press Enter to exit...")
