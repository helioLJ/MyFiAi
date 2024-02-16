from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Import your models here
from .transaction import Transaction
from .user import User
from .insight import Insight