import pandas as pd
import csv
import re
import io
import server.enums.premierleagueenum as ple


class ReadExcelWriteCsv:

    def __write_csv_info(self, from_excel, to_csv):
        liverpool_data = 'excel_data/' + from_excel
        xl = pd.ExcelFile(liverpool_data)
        df1 = xl.parse('Sheet1')

        print(df1)

        with io.open('csv_data/' + to_csv, 'w', encoding="utf-8") as f:
            writer = csv.writer(f)

            for index, row in df1.iterrows():
                row['Score'] = re.sub(
                    " \\([0-9]:[0-9]\\)| \\([0-9]:[0-9], [0-9]:[0-9]\\)| \\([0-9]:[0-9], [0-9]:[0-9], [0-9]:[0-9]\\)| "
                    "pso| aet",
                    "", row['Score'])
                vector = row['Score'].split(':')
                team_goals = vector[0]
                oponent_goals = vector[1]
                if team_goals > oponent_goals:
                    row['Result'] = 'v'
                elif team_goals == oponent_goals:
                    row['Result'] = 'e'
                else:
                    row['Result'] = 'd'
                writer.writerow(row)

        print("Premier League loaded sucessfully into csv files")

    def load_premier_league(self):
        for name in ple.PremierLeague:
            self.__write_csv_info(name.value, name.name)


repo = ReadExcelWriteCsv()
repo.load_premier_league()

