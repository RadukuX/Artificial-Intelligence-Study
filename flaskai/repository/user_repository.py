from flaskai.models import User
from flaskai.repository.db_connection import DbConnection
from flask_bcrypt import Bcrypt


class UserRepository:

    def register_user(self, username, email, password):
        conn = DbConnection().create_connection(DbConnection.database)
        sql = ''' INSERT INTO user(username, email, password) VALUES (?,?,?)'''
        with conn:
            cursor = conn.cursor()
            cursor.execute(sql, [username, email, password])
            return cursor.lastrowid

    def __get_hashed_password(self, email):
        conn = DbConnection().create_connection(DbConnection.database)
        sql = ''' SELECT password FROM user WHERE email=? '''
        with conn:
            cursor = conn.cursor()
            cursor.execute(sql, [email])
            return cursor.fetchall()[0][0]

    def login_user(self, email, password):
        bcrypt = Bcrypt()
        user = User.query.filter_by(email=email).first()
        if bcrypt.check_password_hash(self.__get_hashed_password(email), password) is True:
            conn = DbConnection().create_connection(DbConnection.database)
            sql = ''' SELECT * FROM user WHERE email=? '''
            with conn:
                cursor = conn.cursor()
                cursor.execute(sql, [email])
                if not cursor.fetchall():
                    return [user, False]
                return [user, True]
        else:
            return [user, False]
