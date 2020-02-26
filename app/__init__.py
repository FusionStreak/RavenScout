from flask import Flask
from configure import default_config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(default_config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import routes, models