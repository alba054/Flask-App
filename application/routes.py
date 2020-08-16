from flask import render_template, request, redirect, url_for, session
import json

from application import app, models
from application.controller import DatabaseController, Authenticator


# obj for authenticate login and registration
authenticator = Authenticator()

@app.route('/')
@app.route('/index', methods=['post', 'get'])
def index():
    # print(authenticator.isSuccess)
    engine = DatabaseController('application/data/films.db')
    
    if request.method == 'POST':
        search = request.form.get('search').strip()
        if not search:
            return redirect(url_for('index'))

        exp = f'WHERE title LIKE "%{search}%"'
        results = engine.select('movie', exp=exp)
        movies = []

        for result in results:
            movie = models.Movie(result[1], result[2])
            movie.id = result[0]
            movie.getGenres()
            movies.append(movie)

        # request.method = 'GET'
        
        return render_template('index.html', movies=movies)

    exp = '''
            LIMIT 10
    '''
    results = engine.select('movie', exp=exp)
    movies = []

    for result in results:
        movie = models.Movie(result[1], result[2], result[3])
        movie.id = result[0]
        movie.getGenres()
        movies.append(movie)
    

    return render_template('index.html', movies=movies)

@app.route('/register', methods=['post', 'get'])
def register():
    if 'isSuccess' in session.keys():
        # print(session['email'])
        return redirect(url_for('index'))

    if request.method == 'POST':
        email = request.form.get('email').strip() 
        username = request.form.get('username').strip()
        password = request.form.get('password')
        retype_password = request.form.get('retype-password')
        user = models.User(username, password, email)
        
        if user.register(retype_password):
            return redirect(url_for('login'))
        else:
            return redirect(url_for('error'))



    return render_template('register.html')

@app.route('/login', methods=['post', 'get'])
def login():
    if 'isSuccess' in session.keys():
        return redirect('index')

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        print(username, password)
        
        if authenticator.login(username, password):
            # user = models.User(username, password, authenticator.userEmail)
            session['isSuccess'] = True
            session['username'] = username
            session['userId'] = authenticator.userId
            print(session['userId'])
            return redirect(url_for('index'))
        else:
            return redirect(url_for('error'))

    return render_template('login.html')

@app.route('/popular-movies')
def popular():
    # if authenticator.isSuccess:
    #     return render_template('popular.html')
    engine = DatabaseController('application/data/films.db')
    exp = '''
            ORDER BY score
            LIMIT 30 
    '''
    results = engine.select('movie', exp=exp)
    movies = []

    for result in results:
        movie = models.Movie(result[1], result[2], result[3])
        movie.id = result[0]
        movie.getGenres()
        movies.append(movie)
    
    return render_template('popular.html', movies=movies)

@app.route('/movies')
def movies():
    # if authenticator.isSuccess:
    #     return render_template('movies.html')
    return render_template('movies.html')

@app.route('/favorite')
def favorite():
    if 'isSuccess' not in session:
        return redirect(url_for('index'))
    # if authenticator.isSuccess:
    #     return render_template('favorite.html')

    engine = DatabaseController('application/data/films.db')
    exp = f'''
            JOIN user_movie ON user.id = user_movie.user_id
            JOIN movie ON movie.id = user_movie.movie_id
            WHERE user.id = {session['userId']}
    '''
    results = engine.select('user', 'movie.id, title, release_year', exp)
    movies = []

    for result in results:
        movie = models.Movie(result[1], result[2])
        movie.id = result[0]
        movie.getGenres()
        movies.append(movie)
        

    return render_template('favorite.html', movies=movies)

@app.route('/error')
def error():
    return render_template('error.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/movie/<int:id>/<string:title>')
def movie(id, title):
    engine = DatabaseController('application/data/films.db')
    exp = f'WHERE id = {id} AND title = "{title}"'
    results = engine.select('movie', exp=exp)
    # print(results)
    if results:
        movie = models.Movie(results[0][1], results[0][2], results[0][4], results[0][3])
        movie.id = results[0][0]
        movie.getGenres()
    else:
        return render_template('error.html')
    
    if "isSuccess" in session:
        
        exp = f'WHERE movie_id = {id} AND user_id = {session["userId"]}'
        added = engine.select('user_movie', exp=exp)
        
        return render_template('movie.html', movie=movie, added=added)
        
    return render_template('movie.html', movie=movie)


@app.route('/movie/api/<int:id>/')
def getMovie(id):
    engine = DatabaseController('application/data/films.db')
    exp = f'WHERE id = {id}'
    results = engine.select('movie', exp=exp)
    title = results[0][1]
    release_year = results[0][2]
    id = results[0][0]
    json_dict = {"id":id, "title":title, "release_year":release_year}
    json_str = json.dumps(json_dict)

    return json_str

@app.route('/add-to-favorite/<int:id>/<string:title>')
def added(id, title):
    engine = DatabaseController('application/data/films.db')
    exp = f'WHERE movie_id = {id} AND user_id = {session["userId"]}'
    added = engine.select('user_movie', exp=exp)

    if added:
        engine.delete('user_movie', exp)
    else:
        engine.insertFavoriteMovie((id, session['userId']))

    return redirect(url_for('movie', id=id, title=title))


