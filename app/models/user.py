from . import db

class User(db.Model):
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

    @property
    def is_authenticated(self):
        return self.is_active

    def get_id(self):
        return self.id

    def __repr__(self):
        return f"User('{self.name}', '{self.google_id}')"