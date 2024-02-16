import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    # Usa Database URL se está definido, caso contrário, usa SQLite
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///' + os.path.join(basedir, 'myfi.db'))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    FLASK_SECRET_KEY = os.getenv('FLASK_SECRET_KEY')
    GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
    GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')
    ENVIRONMENT = os.getenv('ENVIRONMENT')