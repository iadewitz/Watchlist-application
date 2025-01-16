import datetime
import pandas as pd
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import sys

# Import custom modules
from src.utils import gui, excel_generator

# # Write Excel
# outFileName = datetime.datetime.today().strftime('%Y%m%d') + "_results"
# generate_excel(finalDataFrame, outFileName)

def onLoadDataEvent(tree):
    global currentData;
    gui.onLoadData(tree);
    currentData = gui.getCurrentData(); # loadButton change the value of currentData
    print(f"currentData updated: {currentData.head()}");

def onDownloadDataEvent(tree, data, nDays):
    global currentData;
    gui.onDownloadData(tree, data, nDays);
    currentData = gui.getCurrentData(); # downloadButton change the value of currentData
    print(f"currentData updated: {currentData.head()}");

def onAddDataEvent(tree, startData):
    global currentData;
    def submitData():
        ticker = tickerEntry.get()
        purchasePrice = float(priceEntry.get())
        purchaseDate = dateEntry.get()

        # Process the data (e.g., add to currentData)
        new_row = pd.DataFrame([[ticker, priceEntry, dateEntry]], columns=["Ticker", "PurchasePrice", "PurchaseDate"])
        currentData = pd.concat([currentData, new_row], ignore_index = True)
        gui.updateTable(tree, currentData)
        addWindow.destroy()

    # Create the window to add data
    addWindow = tk.Toplevel()
    addWindow.title("Add New Data")
    addWindow.geometry("600x450")

    tk.Label(addWindow, text = "Ticker:").pack(pady=5)
    tickerEntry = tk.Entry(addWindow)
    tickerEntry.pack(pady = 5)

    tk.Label(addWindow, text = "Purchase Price:").pack(pady=5)
    priceEntry = tk.Entry(addWindow)
    priceEntry.pack(pady=5)

    tk.Label(addWindow, text = "Purchase Date (YYYY-MM-DD):").pack(pady=5)
    dateEntry = tk.Entry(addWindow)
    dateEntry.pack(pady=5)

    submit_button = tk.Button(addWindow, text = "Submit", command = submitData)
    submit_button.pack(pady = 10)
    
    gui.onAddData(tree, startData);
    currentData = gui.getCurrentData(); # downloadButton change the value of currentData
    print(f"currentData updated: {currentData.head()}");

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
    
    nDays = 252; # Display last nDays of data
    downloadDataButton = tk.Button(root, text = "Download New Data", command = lambda: onDownloadDataEvent(tree, currentData, nDays))
    downloadDataButton.pack(pady = 10)

    addDataButton = tk.Button(root, text = "Add New Data", command = lambda: onAddDataEvent(tree, currentData))
    addDataButton.pack(pady = 10)

    # saveDataButton = tk.Button(root, text = "Save Current View", command = lambda: onSaveDataEvent(tree, currentData))
    # saveDataButton.pack(pady = 10)
    # 
    # computeTotalRow = tk.Button(root, text = "Compute Total", command = lambda: onComputeTotalEvent(tree, currentData))
    # computeTotalRow.pack(pady = 10)

    # plot_button = tk.Button(root, text = "Plot Data", command = on_plot_data)
    # plot_button.pack(pady = 10)

    # computeVaRButton = tk.Button(root, text = "Plot Data", command = lambda: onComputeVaREvent(tree, currentData))
    # computeVaRButton.pack(pady = 10)

    root.mainloop()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"An error occurred: {e}")
        input("Press Enter to exit...")
