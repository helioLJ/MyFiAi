from flask import Flask
from dotenv import load_dotenv
from .database import init_db
from .auth import init_auth
from .routes import init_routes
from .utils import init_utils
from config import Config

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = Config.FLASK_SECRET_KEY
    app.config.from_object(Config)

    init_db(app)
    init_auth(app)
    init_routes(app)
    init_utils(app)

    return app