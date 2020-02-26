from flaskai.repository.db_connection import DbConnection
import csv
from flaskai.enums.premierleagueenum import PremierLeague


class Repository:
    team_dictionary_pl = {'arsenal': 1, 'aston_villa': 2, 'bournemouth': 3, 'brighton': 4, 'burnley': 5, 'chelsea': 6,
                          'crystal_palace': 7, 'everton': 8, 'leicester': 9, 'liverpool': 10, 'manchester_city': 11,
                          'manchester_utd': 12, 'newcastle': 13, 'norwich': 14, 'sheffield': 15, 'southampton': 16,
                          'tottenham': 17, 'watford': 18, 'west_ham': 19, 'wolves': 20}

    def __read_from_csv(self, file_name):
        result_dict = {'Date': '', 'Time': '', 'Oponent': '', 'Score': '', 'Result': '', 'team_id': ''}
        result_list = []
        with open('D:/Artificial Intelligence Study/flaskai/csv_data/' + file_name + '.txt',
                  encoding="utf-8") as csv_file:
            team_name = file_name.replace('_info', '')
            print(self.team_dictionary_pl.get(team_name))
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                result_dict['Date'] = row[0]
                result_dict['Time'] = row[1]
                result_dict['Oponent'] = row[2]
                result_dict['Score'] = row[3]
                result_dict['Result'] = row[4]
                result_dict['team_id'] = self.team_dictionary_pl.get(team_name)
                result_list.append(result_dict.copy())
        return result_list

    def create_results(self, conn, result):
        sql = ''' INSERT INTO results(date,time,opponent,score,result,team_id) VALUES (?,?,?,?,?,?)'''
        cur = conn.cursor()
        cur.execute(sql, result)
        return cur.lastrowid

    def create_teams(self, conn, team_name):
        sql = ''' INSERT INTO team(name) VALUES (?)'''
        cur = conn.cursor()
        print(team_name)
        cur.execute(sql, [team_name])
        return cur.lastrowid

    def load_teams(self):
        database = r'D:\Artificial Intelligence Study\flaskai\test.db'
        conn = DbConnection().create_connection(database)
        with conn:
            for team in PremierLeague:
                team_name = team.name.replace("_info", "")
                self.create_teams(conn, team_name)

    def load_results(self):
        database = r'D:\Artificial Intelligence Study\flaskai\test.db'
        conn = DbConnection().create_connection(database)
        with conn:
            for teams in PremierLeague:
                for result in self.__read_from_csv(teams.name):
                    res = tuple(result.values())
                    self.create_results(conn, res)

    # CALL ONLY IF NO DATA IN DATABASE
    def load_all_db(self):
        self.load_teams()
        self.load_results()

    def register_user(self, username, email, password):
        database = r'D:\Artificial Intelligence Study\flaskai\test.db'
        conn = DbConnection().create_connection(database)
        sql = ''' INSERT INTO user(username, email, password) VALUES (?,?,?)'''
        with conn:
            cur = conn.cursor()
            print('The user ' + username + ' is registering...')
            cur.execute(sql, [username, email, password])
            return cur.lastrowid


repo = Repository()
repo.register_user('bla', 'email', '123')