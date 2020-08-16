from application.controller import DatabaseController

class User:
    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email
    
    def register(self, retype_password):
        engine = DatabaseController('application/data/films.db')
        
        exp = f'WHERE email = "{self.email}" OR username = "{self.username}"'
        
        isSuccess = (len(engine.select('user', exp=exp)) == 0
                     and ((len(self.username) != 0 or len(self.password) != 0
                         or len(self.email) != 0) and (self.password == retype_password))
        )
        # print(len(engine.select(record)))

        if isSuccess:
            engine.insert(self)
            
            return True
        
        return False
        


class Movie:
    def __init__(self, title, release_year, synopsis=None, score=0):
        self.title = title
        self.release_year = release_year
        self.score = score
        self.synopsis = synopsis
        

    def getGenres(self):
        engine = DatabaseController('application/data/films.db')
        exp = f'''JOIN movie_genre ON genre.id = movie_genre.genre_id WHERE movie_genre.movie_id = {self.id}'''
        results = engine.select('genre', exp=exp, attr='name')
        self.genres = []

        for genre in results:
            self.genres.append(genre[0])




# if __name__ == "__main__":
    
