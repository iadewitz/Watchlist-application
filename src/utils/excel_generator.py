import datetime
import pandas

def generateExcel(dataFrame, folder):
    """
    Writes the given DataFrame to an Excel file.

    Parameters:
    dataFrame (pd.DataFrame): The DataFrame to write to Excel.
    folder (str): The path where the Excel file will be saved.
    """
    outFileName = "/" + datetime.datetime.today().strftime('%Y%m%d') + "_results" + ".xlsx";
    filePath = folder + outFileName;
    dataFrame.to_excel(filePath, index = False);