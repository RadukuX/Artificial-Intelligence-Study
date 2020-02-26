import pandas as pd
import csv
import re
import io
import flaskai.enums.premierleagueenum as ple


class ReadExcelWriteCsv:

    def __write_csv_info(self, from_excel, to_csv):
        liverpool_data = 'excel_data/' + from_excel
        xl = pd.ExcelFile(liverpool_data)
        df1 = xl.parse('Sheet1')

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

    def load_premier_league(self):
        for name in ple.PremierLeague:
            self.__write_csv_info(name.value, name.name)
            self.__eliminate_white_spaces(name.name, name.name)
        print("Premier League loaded sucessfully into csv files")

    def __eliminate_white_spaces(self, in_file, out_file):
        with open('csv_data/' + in_file, 'r', encoding='utf-8') as inFile, \
                open('csv_data/' + out_file + '.txt', 'w', encoding='utf-8') as outFile:
            for line in inFile:
                if line.strip():
                    outFile.write(line)


repo = ReadExcelWriteCsv()
repo.load_premier_league()

