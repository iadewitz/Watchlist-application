import os

def generate_excel(dataFrame, outFileName):
    """
    Writes the given DataFrame to an Excel file.

    Parameters:
    dataFrame (pd.DataFrame): The DataFrame to write to Excel.
    file_path (str): The path where the Excel file will be saved.
    """
    filePath = os.getcwd() + "\\" + "out" + "\\" + outFileName + ".xlsx"
    dataFrame.to_excel(filePath, index = False)