import sqlite3
from sqlite3 import Error

from application import models

class DatabaseController:
    def __init__(self, db):
        self.db = db

    def insert(self, table):
        table_name = table.__class__.__name__
        fields = list(table.__dict__.keys())
        values = tuple(table.__dict__.values())

        sql = f'''INSERT INTO {table_name} ({",".join(fields)}) 
                VALUES ({",".join(["?" for i in range(len(fields))])})
        '''
        # print(sql)
        conn = sqlite3.connect(self.db)
        cur = conn.cursor()
        cur.execute(sql, values)
        print('inserting completed')
        conn.commit()
        conn.close()

    def insertFavoriteMovie(self, user_movie):
        conn = sqlite3.connect(self.db)
        cur = conn.cursor()
        sql = 'INSERT INTO user_movie (movie_id, user_id) VALUES (?, ?)'
        cur.execute(sql, user_movie)
        conn.commit()
        conn.close()

    def select(self, table_name, attr='*', exp=None):
        # table_name = table.__class__.__name__
        if not exp:
            sql = f'SELECT {attr} FROM {table_name}'
        else:
            sql = F'SELECT {attr} FROM {table_name} {exp}'
        
        conn = sqlite3.connect(self.db)
        cur = conn.cursor()
        cur.execute(sql)
        results = cur.fetchall()
        conn.commit()
        conn.close()
        
        return results
    
    def delete(self, table_name, exp):
        sql = f'DELETE FROM {table_name} {exp}'
        conn = sqlite3.connect(self.db)
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
        conn.close()

class Authenticator:

    
    def login(self, username, password):
        engine = DatabaseController('application/data/films.db')
        exp = f'WHERE username = "{username}" AND password = "{password}"'
        
        # print(engine.select('user', exp))
        results = engine.select('user', exp=exp)
        isSuccess = len(results) > 0
    
        if isSuccess:
            self.userEmail = results[0][2]
            self.userId = results[0][0]

        return isSuccess


# if __name__ == "__main__":
#     engine = DatabaseController('data/films.db')
#     results = engine.select('movie')
#     print(results)

        
