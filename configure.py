import os
basedir = os.path.abspath(os.path.dirname(__file__))

class default_config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-know'
    SQL_ALCHEMY_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATICATIONS = False