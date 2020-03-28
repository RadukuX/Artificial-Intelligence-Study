from flaskai.models import User
from flaskai.repository.db_connection import DbConnection
from flask_bcrypt import Bcrypt


class UserRepository:

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
            return cursor_fetch[0][0]

    def login_user(self, email, password):
        bcrypt = Bcrypt()
        user = User.query.filter_by(email=email).first()
        if bcrypt.check_password_hash(self.__get_hashed_password(email), password) is True:
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

