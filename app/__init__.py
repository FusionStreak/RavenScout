from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from configure import default_config

app = Flask(__name__)
app.config.from_object(default_config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
app.config['SQLALCHEMY_TRACK_MODIFICATICATIONS'] = False

from app import routes, models