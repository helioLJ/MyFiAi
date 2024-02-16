from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_dance.contrib.google import make_google_blueprint
from flask_login import LoginManager, current_user
from flask_migrate import Migrate

from dotenv import load_dotenv
import os

from config import Config
from .models import db, User, UserStorage

load_dotenv()
login_manager = LoginManager()
migrate = Migrate()
@login_manager.user_loader
def load_user(user_id):
    print(f"user_id: {user_id}")
    print(f"User: {User.query.filter(User.google_id == user_id).first()}")
    return User.query.filter(User.google_id == user_id).first()

if os.getenv('ENVIRONMENT') == 'development':
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

app = Flask(__name__)
login_manager.init_app(app)

app.config['SECRET_KEY'] = os.getenv("FLASK_SECRET_KEY")
app.config.from_object(Config)

def get_user_id():
    if current_user.is_authenticated:
        return current_user.get_id()
    return None

google_blueprint = make_google_blueprint(
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    scope=[
        "https://www.googleapis.com/auth/userinfo.email",
        "https://www.googleapis.com/auth/userinfo.profile",
        "openid"
    ],
    offline=True,
    reprompt_consent=True,
)

app.register_blueprint(google_blueprint, url_prefix="/auth")

db.init_app(app)
migrate.init_app(app, db)

with app.app_context():
    db.create_all()

from app.routes import transaction
from app.routes import dashboard