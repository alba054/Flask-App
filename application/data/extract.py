import os

import sqlite3
import csv
import json

db = "films.db"
file = 'tmdb_5000_movies.csv'

# input all genre to genre table

# with open(file, encoding='utf-8') as raw_file:
#     csv_dict = csv.DictReader(raw_file)
#     conn = sqlite3.connect(db)
#     cur = conn.cursor()
#     # movie_without_genre = []
#     lists_genre = []
#     for csv in csv_dict:
#         genres = json.loads(csv['genres'])

#         for genre in genres:
#             # if genre['name'] not in lists_genre:
#             #     lists_genre.append(genre['name'])
#             conn = sqlite3.connect(db)
#             cur = conn.cursor()
#             sql = '''
#                     INSERT INTO genre (id, name) 
#                     VALUES (:id, :name)
#             '''
#             try:
#                 cur.execute(sql, genre)
#                 print('inserting completed')
#                 conn.commit()
#             except sqlite3.IntegrityError:
#                 pass


#     cur.close()
#     conn.close() 

# input all movie into movie table

# with open(file, encoding='utf-8') as raw_file:
#     csv_dict = csv.DictReader(raw_file)
#     conn = sqlite3.connect(db)
#     cur = conn.cursor()


#     for csv in csv_dict:
#         if csv['genres'] != '[]':
#             try:
#                 release_year = csv["release_date"].split('/')[2]
#                 movie = {
#                     "id":csv['id'],
#                     "title":csv['original_title'],
#                     "release_year":release_year,
#                     "synopsis":csv['overview']
#                 }
#                 sql = '''
#                         INSERT INTO movie (id, title, release_year, synopsis)
#                         VALUES (:id, :title, :release_year, :synopsis)
#                 '''

#                 cur.execute(sql, movie)
#                 print('inserting completed')
#             except IndexError:
#                 pass

# input genre related to movie

# with open(file, encoding='utf-8') as raw_file:
#     raw_csv = csv.DictReader(raw_file)
#     conn = sqlite3.connect(db)
#     cur = conn.cursor()
    
#     for csv in raw_csv:
#         if csv['genres'] != '[]':
#             try:
#                 release_year = csv["release_date"].split('/')[2]
#                 genres = json.loads(csv['genres'])
#                 movie_id = csv['id']

#                 for genre in genres:
#                     sql = '''
#                             INSERT INTO movie_genre (movie_id, genre_id)
#                             VALUES (?, ?)
#                     '''
#                     cur.execute(sql, (movie_id, genre['id']))
#                     print('inserting completed')
#             except IndexError:
#                 pass
        

#     conn.commit()
#     cur.close()
#     conn.close()

    
#     conn.commit()
#     cur.close()
#     conn.close()

# conn = sqlite3.connect(db)
# cur = conn.cursor()
# sql = '''
#         INSERT INTO genre (id, name) 
#         VALUES (:id, :name)
# '''
# try:
#     cur.execute(sql, {"id":1, "name":"action"})
#     print('inserting completed')
#     conn.commit()
# except sqlite3.IntegrityError:
#     pass    
        