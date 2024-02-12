from .. import app
from flask import render_template

from ..services.transaction import get_current_month_transactions

@app.route('/')
def index():
    transactions = get_current_month_transactions()
    return render_template('index.html', transactions=transactions)
