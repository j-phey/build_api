from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    
    # Creating the flask app object - this is the core of our app!
    app = Flask(__name__)

    # configuring our app:
    app.config.from_object("config.app_config")

    # creating a generic db object that we can import into our models code
    # creating our database object! This allows us to use our ORM
    db.init_app(app)
   
    return app