# auth.py
from flask_login import LoginManager
from .models import User

login_manager = LoginManager()
login_manager.login_view = 'login_page'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

def init_auth(app):
    login_manager.init_app(app)