import pandas as pd

class ReadExcelWriteCsv:

    def liverpool_info(self):
        liverpool_data = 'excel_data/Liverpool Results.xlsx'
        xl = pd.ExcelFile(liverpool_data)
        df1 = xl.parse('Sheet2')
        print(df1)

repo = ReadExcelWriteCsv()
repo.liverpool_info()