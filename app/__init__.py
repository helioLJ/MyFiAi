from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from .models import db

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
app.config.from_object(Config)
db.init_app(app)

with app.app_context():
    db.create_all()

from app.routes import transaction
from app.routes import dashboard