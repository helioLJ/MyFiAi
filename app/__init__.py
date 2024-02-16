from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

from dotenv import load_dotenv
import os

from config import Config
from .models import db, User

load_dotenv()
migrate = Migrate()

if os.getenv('ENVIRONMENT') == 'development':
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("FLASK_SECRET_KEY")
app.config.from_object(Config)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

db.init_app(app)
migrate.init_app(app, db)

with app.app_context():
    db.create_all()

from app.routes import transaction
from app.routes import dashboard