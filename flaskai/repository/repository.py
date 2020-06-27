import re
from flaskai.repository.db_connection import DbConnection
import csv
import numpy as np
from flaskai.enums.premierleagueenum import PremierLeague


class Repository:

    team_dictionary_pl = {'arsenal': 1, 'aston_villa': 2, 'bournemouth': 3, 'brighton': 4, 'burnley': 5, 'chelsea': 6,
                          'crystal_palace': 7, 'everton': 8, 'leicester': 9, 'liverpool': 10, 'manchester_city': 11,
                          'manchester_united': 12, 'newcastle': 13, 'norwich': 14, 'sheffield': 15, 'southampton': 16,
                          'tottenham': 17, 'watford': 18, 'west_ham': 19, 'wolves': 20}

    help_dicty_pl = {"chelsea": 6, "liverpool": 10, "manchester_united": 12}

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

    def __read_from_extra_csv(self, filename):
        result_dict = {'year': '', 'investment': '', 'age': '', 'wins': '', 'draws': '', 'defeats': '', 'goals': '', 'place': '', 'team_id': ''}
        result_list = []
        with open('D:/Artificial Intelligence Study/flaskai/csv_data/csv_extra_data/' + filename + '.txt', encoding='utf-8') as csv_file:
            team_name = str(filename)
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                result_dict['year'] = row[0]
                result_dict['investment'] = row[1]
                result_dict['age'] = row[2]
                result_dict['wins'] = row[3]
                result_dict['draws'] = row[4]
                result_dict['defeats'] = row[5]
                result_dict['goals'] = row[6]
                result_dict['place'] = row[7]
                result_dict['team_id'] = self.team_dictionary_pl.get(team_name)
                result_list.append(result_dict.copy())
        return result_list

    def create_results(self, conn, result):
        sql = ''' INSERT INTO results(date,time,opponent,score,result,team_id) VALUES (?,?,?,?,?,?)'''
        cursor = conn.cursor()
        cursor.execute(sql, result)
        cursor_lastrow = cursor.lastrowid
        cursor.close()
        return cursor_lastrow

    def create_teams(self, conn, team_name):
        sql = ''' INSERT INTO team(name) VALUES (?)'''
        cursor = conn.cursor()
        print(team_name)
        cursor.execute(sql, [team_name])
        cursor_lastrow = cursor.lastrowid
        cursor.close()
        return cursor_lastrow

    def create_extra_data(self, conn, result):
        sql = ''' INSERT INTO extra_data(year,investment,age,wins,draws,defeats,goals,place,team_id) VALUES (?,?,?,?,?,?,?,?,?) '''
        cursor = conn.cursor()
        cursor.execute(sql, result)
        cursor_lastrow = cursor.lastrowid
        cursor.close()
        return cursor_lastrow

    def load_teams(self):
        conn = DbConnection().create_connection(DbConnection.database)
        with conn:
            for team in PremierLeague:
                team_name = team.name.replace("_info", "")
                self.create_teams(conn, team_name)

    def load_results(self):
        conn = DbConnection().create_connection(DbConnection.database)
        with conn:
            for teams in PremierLeague:
                for result in self.__read_from_csv(teams.name):
                    res = tuple(result.values())
                    self.create_results(conn, res)

    def load_extra_data(self):
        conn = DbConnection().create_connection(DbConnection.database)
        with conn:
            for team in self.help_dicty_pl:
                for result in self.__read_from_extra_csv(team):
                    res = tuple(result.values())
                    self.create_extra_data(conn, res)

    # CALL ONLY IF NO DATA IN DATABASE
    def load_all_db(self):
        self.load_teams()
        self.load_results()
        self.load_extra_data()

    def get_all_teams(self):
        conn = DbConnection().create_connection(DbConnection.database)
        sql = ''' SELECT * FROM team '''
        with conn:
            cursor = conn.cursor()
            cursor.execute(sql, [])
            all_teams = cursor.fetchall()
            cursor.close()
            return all_teams

    def get_team_result(self, team_id):
        conn = DbConnection().create_connection(DbConnection.database)
        sql = ''' SELECT * FROM results WHERE team_id = ? '''
        with conn:
            cursor = conn.cursor()
            cursor.execute(sql, [team_id])
            all_teams_encoded = []
            for i, row in enumerate(cursor):
                t = [row[0], row[1], row[2], row[3], row[4], row[5]]
                all_teams_encoded.append(t)
            cursor.close()
            return np.asarray(all_teams_encoded)

    def get_results_for_a_specific_team(self, team_a_id, team_b):
        conn = DbConnection().create_connection(DbConnection.database)
        sql = ''' SELECT * FROM results WHERE team_id=? AND opponent=?'''
        with conn:
            cursor = conn.cursor()
            cursor.execute(sql, [team_a_id, team_b])
            all_teams = []
            for i, row in enumerate(cursor):
                t = [row[0], row[1], row[2], row[3], row[4], row[5]]
                all_teams.append(t)
            cursor.close()
            return np.asarray(all_teams)

    def get_extra_data(self, team_id):
        conn = DbConnection().create_connection(DbConnection.database)
        sql = ''' SELECT * FROM extra_data WHERE team_id=? '''
        with conn:
            cursor = conn.cursor()
            cursor.execute(sql, [team_id])
            all_data = []
            for i, row in enumerate(cursor):
                investments = int(row[2])
                age = int(row[3])
                wins = int(row[4])
                equals = int(row[5])
                defeats = int(row[6])
                goals = int(row[7])
                place = int(row[8])
                t = [investments, age, wins, equals, defeats, goals, place]
                all_data.append(t)
            cursor.close()
            return np.asarray(all_data)

    def get_wins_equals_defeats(self, my_team, oponent):
        conn = DbConnection().create_connection(DbConnection.database)
        sql_wins = ''' SELECT result FROM results WHERE team_id=? AND opponent=? AND result="v" '''
        sql_equals = ''' SELECT result FROM results WHERE team_id=? AND opponent=? AND result="e" '''
        sql_defeats = ''' SELECT result FROM results WHERE team_id=? AND opponent=? AND result="d" '''
        wins_list = []
        equals_list = []
        defeats_list = []
        data = []
        with conn:
            cursor1 = conn.cursor()
            cursor2 = conn.cursor()
            cursor3 = conn.cursor()
            cursor1.execute(sql_wins, [self.team_dictionary_pl.get(my_team), oponent])
            cursor2.execute(sql_defeats, [self.team_dictionary_pl.get(my_team), oponent])
            cursor3.execute(sql_equals, [self.team_dictionary_pl.get(my_team), oponent])
            for i, row in enumerate(cursor1):
                wins_list.append(row)
            for i, row in enumerate(cursor2):
                defeats_list.append(row)
            for i, row in enumerate(cursor3):
                equals_list.append(row)
        nr_of_wins = len(wins_list)
        nr_of_equals = len(equals_list)
        nr_of_defeats = len(defeats_list)
        data.append(nr_of_wins)
        data.append(nr_of_equals)
        data.append(nr_of_defeats)
        cursor1.close()
        cursor2.close()
        cursor3.close()
        return data

    def get_data(self, my_team, oponent):
        conn = DbConnection().create_connection(DbConnection.database)
        sql = ''' SELECT score FROM results WHERE team_id=? AND opponent=?'''
        with conn:
            cursor = conn.cursor()
            print(self.team_dictionary_pl.get(my_team))
            cursor.execute(sql, [self.team_dictionary_pl.get(my_team), oponent])
            score = []
            g_g = []
            g_t = []
            data = []
            for i, row in enumerate(cursor):
                sc = row[0]
                goals_given = sc.split(':')[0]
                g_g.append(int(goals_given))
                goals_taken = sc.split(':')[1]
                g_t.append(int(goals_taken))
                score.append(sc)
            total_of_goals_given = sum(g_g)
            total_of_goals_take = sum(g_t)
            data.append(total_of_goals_given)
            data.append(total_of_goals_take)
            data.extend(self.get_wins_equals_defeats(my_team, oponent))
            cursor.close()
            # goals_given goals_taken nr_of_wins nr_of_equals nr_of_defeats
            return data

    def get_goals_result(self, my_team, oponent):
        conn = DbConnection().create_connection(DbConnection.database)
        sql = ''' SELECT score,result FROM results WHERE team_id=? AND opponent=?'''
        with conn:
            cursor = conn.cursor()
            score_result = []
            cursor.execute(sql, [self.team_dictionary_pl.get(my_team), oponent])
            for i, row in enumerate(cursor):
                li = []
                score = row[0].split(':')
                li.append(score[0])
                li.append(score[1])
                li.append(row[1])
                score_result.append(li)
            cursor.close()
            return score_result