from application import app
from application import routes

# app configuration
app.config['SECRET_KEY'] = 'this is string'

if __name__ == "__main__":
    app.run()