from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import config

def create_app(configName : str):
    app = Flask(__name__)
    app.config.from_object(config[configName])
    config[configName].init_app(app)
    return app

def create_db(app : Flask):
    db = SQLAlchemy(app)
    return db

def create_migrate(app : Flask, db : SQLAlchemy):
    migrate = Migrate(app, db)
    return migrate

