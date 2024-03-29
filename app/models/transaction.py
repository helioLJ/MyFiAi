from . import db

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    transaction_type = db.Column(db.String(120), nullable=False)
    category = db.Column(db.String(120), nullable=False)
    details = db.Column(db.String(120), nullable=False)
    expected_date = db.Column(db.DateTime, nullable=True)
    payday = db.Column(db.DateTime, nullable=True)
    recurrence = db.Column(db.String(120), nullable=False)
    expected_value = db.Column(db.Float, nullable=False)
    paid_value = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.String(120), db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'<Transaction {self.name} - R$ {self.paid_value}>'