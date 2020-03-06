from flaskai.repository.db_connection import DbConnection


class UserRepository:

    def register_user(self, username, email, password):
        conn = DbConnection().create_connection(DbConnection.database)
        sql = ''' INSERT INTO user(username, email, password) VALUES (?,?,?)'''
        with conn:
            cursor = conn.cursor()
            cursor.execute(sql, [username, email, password])
            return cursor.lastrowid

    def login_user(self, email, password):
        conn = DbConnection().create_connection(DbConnection.database)
        sql = ''' SELECT * FROM user WHERE email=? AND password=? '''
        with conn:
            cursor = conn.cursor()
            cursor.execute(sql, [email, password])
            if not cursor.fetchall():
                return False
            return True
