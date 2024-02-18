from . import db

class User(db.Model):
    id = db.Column(db.String(120), primary_key=True) # Google ID
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    profile_pic_url = db.Column(db.String(500))
    is_premium = db.Column(db.Boolean, default=True)
    google_token = db.Column(db.String(500), nullable=False)
    refresh_token = db.Column(db.String(500))
    is_active = db.Column(db.Boolean, default=True)

    transactions = db.relationship('Transaction', backref='user', lazy=True)
    insights = db.relationship('Insight', backref='user', lazy=True)

    @property
    def is_authenticated(self):
        return self.is_active

    def get_id(self):
        return self.id

    def __repr__(self):
        return f"User('{self.name}', '{self.id}')"