from flask_migrate import Migrate
from .models import db

migrate = Migrate()

def init_db(app):
    db.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        db.create_all()