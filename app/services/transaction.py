from datetime import datetime
from ..models import Transaction, db

def get_current_month_transactions():
    current_month = datetime.now().month
    transactions = Transaction.query.filter(db.extract('month', Transaction.payday) == current_month).all()
    return transactions