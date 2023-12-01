from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow # Marshmallow works by creating a Marshmallow object that does the work of generating schemas
from flask_bcrypt import Bcrypt # allows generating objects that will allow authenticated requests by hashing the password
from flask_jwt_extended import JWTManager  # generates and manages the token

db = SQLAlchemy()
app = Flask(__name__)

# set the database URI via SQLAlchemy, 
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql+psycopg2://db_dev:123456@localhost:5432/trello_clone_db"

#create the database object
db = SQLAlchemy(app)
# Creates the Marshmallow object
ma = Marshmallow()
# Creates the Bycrypt object
bcrypt = Bcrypt()
# Creates the JWTManager object
jwt = JWTManager()

# class Card(db.Model):
#     # define the table name for the db
#     __tablename__= "cards"
#     # Set the primary key, we need to define that each attribute is also a column in the db table, remember "db" is the object we created in the previous step.
#     id = db.Column(db.Integer,primary_key=True)
#     # Add the rest of the attributes. 
#     title = db.Column(db.String())
#     description = db.Column(db.String())
#     date = db.Column(db.Date())
#     status = db.Column(db.String())
#     priority = db.Column(db.String())

# create app's cli command named create, then run it in the terminal as "flask create", 
# it will invoke create_db function
# @app.cli.command("create")
# def create_db():
#     db.create_all()
#     print("Tables created")

def create_app():
    # using a list comprehension and multiple assignment 
    # to grab the environment variables we need
    
    # Creating the flask app object - this is the core of our app!
    app = Flask(__name__)

    # configuring our app:
    app.config.from_object("config.app_config")
    # show the columns in the right order instead of alphabetically
    app.json.sort_keys = False

    # creating our database object! This allows us to use our ORM
    db.init_app(app)

    # creating our marshmallow object! This allows us to use schemas
    ma.init_app(app)

    #creating the jwt and bcrypt objects! this allows us to use authentication
    bcrypt.init_app(app)
    jwt.init_app(app)

    # register this blueprint on app in main.py.
    from commands import db_commands
    app.register_blueprint(db_commands)

    # import the controllers and activate the blueprints
    from controllers import registerable_controllers

    for controller in registerable_controllers:
        app.register_blueprint(controller)
    
    return app