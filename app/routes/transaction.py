from .. import app
from .. import filters

from flask import render_template, redirect, url_for

from ..services.transaction import get_month_transactions, insert_transaction, edit_transaction, delete_transaction

@app.route('/')
def index():
    transactions, next_url, prev_url, month = get_month_transactions()
    return render_template('index.html', transactions=transactions, next_url=next_url, prev_url=prev_url, current_month=month)

@app.route('/transaction', methods=['POST'])
def create():
    insert_transaction()
    return redirect(url_for('index'))

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    edit_transaction(id)
    return redirect(url_for('index'))

@app.route('/delete_transaction/<int:id>', methods=['GET', 'POST'])
def delete(id):
    delete_transaction(id)
    return redirect(url_for('index'))