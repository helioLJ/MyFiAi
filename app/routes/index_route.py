from datetime import datetime
from flask import render_template, redirect, url_for
from ..forms import TransactionForm
from ..models import Transaction, db
from .. import app

@app.route('/')
def index():
    return render_template('index.html')

from datetime import datetime

@app.route('/new_transaction', methods=['GET', 'POST'])
def new_transaction():
    form = TransactionForm()
    new_transaction = Transaction(
        name='Açaí',
        category='Alimentação',
        details='Saboroso açaí com granola e banana.',
        expected_date=datetime.utcnow(),  # provide a valid date
        payday=datetime.utcnow(),  # provide a valid date
        recurrence='Semanalmente',
        expected_value=10.0,
        paid_value=15.0
    )
    db.session.add(new_transaction)
    db.session.commit()

    return render_template('index.html', form=form)