from flask_login import UserMixin
from flask_dance.consumer.storage.sqla import SQLAlchemyStorage

from . import db

class User(UserMixin, db.Model):
    id = db.Column(db.String(120), primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    google_id = db.Column(db.String(120), nullable=False)
    google_token = db.Column(db.String(500), nullable=False)
    refresh_token = db.Column(db.String(500))
    profile_pic_url = db.Column(db.String(500))
    is_active = db.Column(db.Boolean, default=True)

    __table_args__ = (
        db.UniqueConstraint('google_id', name='uix_1'),
    )

    def __repr__(self):
        return f"User('{self.name}', '{self.google_id}')"
    
    def get_id(self):
        return self.google_id
    
class UserStorage(SQLAlchemyStorage):
    def __init__(self, *args, **kwargs):
        super(UserStorage, self).__init__(model=User, session=db.session, *args, **kwargs)

    def get(self, blueprint):
        user = User.query.get(self.user_id)
        if user:
            return {"access_token": user.google_token, "refresh_token": user.refresh_token}

    def set(self, blueprint, token):
        user = User.query.get(self.user_id)
        if user:
            user.google_token = token["access_token"]
            user.refresh_token = token["refresh_token"]
            db.session.commit()