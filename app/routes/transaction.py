# routes/transaction.py
from flask import render_template, redirect, url_for
from flask_login import login_required

from ..services.transaction import get_month_transactions, insert_transaction, edit_transaction, delete_transaction, generate_insight

def init_transaction_routes(app):
    @app.route('/')
    @login_required
    def index():
        data = get_month_transactions()
        return render_template('index.html', **data)

    @app.route('/transaction', methods=['POST'])
    @login_required
    def create():
        insert_transaction()
        return redirect(url_for('index'))

    @app.route('/edit/<int:id>', methods=['GET', 'POST'])
    @login_required
    def edit(id):
        edit_transaction(id)
        return redirect(url_for('index'))

    @app.route('/delete/<int:id>', methods=['GET', 'POST'])
    @login_required
    def delete(id):
        delete_transaction(id)
        return redirect(url_for('index'))
    
    @app.route('/generate_insight', methods=['POST'])
    @login_required
    def generate_insight():
        generate_insight()
        return redirect(url_for('index'))