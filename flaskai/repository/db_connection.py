import sqlite3
from sqlite3 import Error


class DbConnection:
    database = r'D:\Artificial Intelligence Study\flaskai\test.db'

    def create_connection(self, db_file):
        conn = None
        try:
            conn = sqlite3.connect(db_file)
        except Error as e:
            print(e)
        return conn
