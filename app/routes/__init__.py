from .transaction import init_transaction_routes
from .dashboard import init_dashboard_routes
from .login import init_login_routes
from .profile import init_profile_routes
from ..database import db

def init_routes(app):
    init_transaction_routes(app)
    init_dashboard_routes(app)
    init_login_routes(app, db)
    init_profile_routes(app)