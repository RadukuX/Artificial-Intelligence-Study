from flaskai.models import User
from flaskai.repository.db_connection import DbConnection
from flask_bcrypt import Bcrypt


class UserRepository:

    team_dictionary_pl = {'arsenal': 1, 'aston_villa': 2, 'bournemouth': 3, 'brighton': 4, 'burnley': 5, 'chelsea': 6,
                          'crystal_palace': 7, 'everton': 8, 'leicester': 9, 'liverpool': 10, 'manchester_city': 11,
                          'manchester_united': 12, 'newcastle': 13, 'norwich': 14, 'sheffield': 15, 'southampton': 16,
                          'tottenham': 17, 'watford': 18, 'west_ham': 19, 'wolves': 20}


    def register_user(self, username, email, password, admin):
        conn = DbConnection().create_connection(DbConnection.database)
        sql = ''' INSERT INTO user(username, email, password, admin) VALUES (?,?,?,?)'''
    
        sql1 = '''  '''
        with conn:
            cursor = conn.cursor()
            cursor.execute(sql, [username, email, password, admin])
            cursor_last_row = cursor.lastrowid
            cursor.close()
            return cursor_last_row

    def __get_hashed_password(self, email):
        conn = DbConnection().create_connection(DbConnection.database)
        sql = ''' SELECT password FROM user WHERE email=? '''
        with conn:
            cursor = conn.cursor()
            cursor.execute(sql, [email])
            cursor_fetch = cursor.fetchall()
            cursor.close()
            return cursor_fetch

    def login_user(self, email, password):
        bcrypt = Bcrypt()
        user = User.query.filter_by(email=email).first()
        if not self.__get_hashed_password(email):
            return [user, False]
        if bcrypt.check_password_hash(self.__get_hashed_password(email)[0][0], password) is True:
            conn = DbConnection().create_connection(DbConnection.database)
            sql = ''' SELECT * FROM user WHERE email=? '''
            with conn:
                cursor = conn.cursor()
                cursor.execute(sql, [email])
                cursor_fetch = cursor.fetchall()
                cursor.close()
                if not cursor_fetch:
                    return [user, False]
                return [user, True]
        else:
            return [user, False]

    def __function_to_return_user_id(self, email):
        conn = DbConnection().create_connection(DbConnection.database)
        sql = ''' SELECT id FROM user WHERE email=?'''
        with conn:
            cursor = conn.cursor()
            cursor.execute(sql, [email])
            cursor_fetch = cursor.fetchall()
            cursor.close()
            return cursor_fetch[0][0]

    def add_teams(self, team_list, current_user_email):
        print("list in repository : " + str(team_list) + current_user_email)
        user_id = self.__function_to_return_user_id(current_user_email)
        sql = ''' INSERT INTO subscriptions(user_id, team_id) VALUES(?,?)'''
        conn = DbConnection().create_connection(DbConnection.database)
        if not team_list:
            return False
        else: 
            with conn:
                cursor = conn.cursor()
                for team in team_list:
                    team_id = self.team_dictionary_pl.get(team)
                    cursor.execute(sql, [user_id, team_id])
                cursor.close()
                return True

    def check_subscriptions(self, email):
        user_id = self.__function_to_return_user_id(email)
        sql = ''' SELECT team_id FROM subscriptions WHERE user_id=? '''
        conn = DbConnection().create_connection(DbConnection.database)
        result = []
        with conn:
            cursor = conn.cursor()
            cursor.execute(sql, [user_id])
            team_list = cursor.fetchall()
            cursor.close()
            for team in team_list:
                result.append(team[0])
            return result