from . import db

class Insight(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    month = db.Column(db.Integer(), nullable=False) # Month and year
    text = db.Column(db.String(5000), nullable=False)  # Increase the maximum length to 5000
    
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)

    user_id = db.Column(db.String(120), db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'<Transaction {self.month}>'