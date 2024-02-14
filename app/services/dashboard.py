import os

from ..models import Transaction, db

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pandas as pd
import sqlalchemy as sql
import numpy as np

def get_dashboard_data():
    # Define the path to your SQLite database file
    database_file = 'sqlite:///myfi.db'

    # Create the SQLAlchemy engine
    engine = sql.create_engine(database_file)

    # Fetch all transactions
    query = db.session.query(Transaction)
    sql_query = str(query.statement.compile(engine))

    transactions = pd.read_sql_query(sql_query, engine)

    # Get unique transaction types and categories
    transaction_types = transactions['transaction_type'].unique()
    categories = transactions['category'].unique()

    # Initialize a dictionary to hold the sums for each category and transaction type
    category_sums = {category: np.zeros(len(transaction_types)) for category in categories}

    # Sum the paid_value for each transaction type for each category
    for i, transaction_type in enumerate(transaction_types):
        for category in categories:
            category_sums[category][i] = transactions[(transactions['transaction_type'] == transaction_type) & (transactions['category'] == category)]['paid_value'].sum()

    get_bar_label(transaction_types, category_sums)
    get_bar_label_input_vs_output(transactions)
    get_bar_label_balance(transactions)
    save_pie_chart('Renda', transactions)
    save_pie_chart('Despesa', transactions)
    save_pie_chart('Ativo', transactions)
    save_pie_chart('Passivo', transactions)

    return

def get_bar_label(transaction_types, category_sums):
    width = 0.6  # the width of the bars: can also be len(x) sequence

    fig, ax = plt.subplots()
    bottom = np.zeros(len(transaction_types))

    for category, category_sum in category_sums.items():
        p = ax.bar(transaction_types, category_sum, width, label=category, bottom=bottom)
        bottom += category_sum

    ax.set_title('Valores totais por categoria e tipo de transação')
    ax.legend()

    # Format y axis as currency
    formatter = ticker.FuncFormatter(lambda x, pos: 'R$ {:.0f}'.format(x))
    ax.yaxis.set_major_formatter(formatter)

    plt.show()

    # Ensure the directory exists
    os.makedirs('app/static/images', exist_ok=True)

    plt.savefig('app/static/images/transaction_counts_by_category_and_type.png')

def get_bar_label_input_vs_output(transactions):
    fig, ax = plt.subplots()

    # Group transaction types
    transaction_types = ['Despesa', 'Ativo', 'Passivo', 'Renda']

    # Calculate sums for each group
    category_sums_grouped = {
        'Despesa': transactions[(transactions['transaction_type'] == 'Despesa')]['paid_value'].sum(),
        'Ativo': transactions[(transactions['transaction_type'] == 'Ativo')]['paid_value'].sum(),
        'Passivo': transactions[(transactions['transaction_type'] == 'Passivo')]['paid_value'].sum(),
    }

    # Create the first bar for 'Despesa', 'Ativo', 'Passivo'
    bottom = 0
    for category in ['Despesa', 'Ativo', 'Passivo']:
        category_sum = category_sums_grouped[category]
        p = ax.bar(0, category_sum, 0.35, bottom=bottom, label=category)
        bottom += category_sum

        # Add the values inside the bars
        for rect in p:
            height = rect.get_height()
            ax.text(rect.get_x() + rect.get_width() / 2., bottom,
                    'R$ {:.0f}'.format(height),
                    ha='center', va='bottom')

    # Calculate sums for each 'Renda' category
    renda_categories = transactions[transactions['transaction_type'] == 'Renda']['category'].unique()
    renda_sums_grouped = {category: transactions[(transactions['transaction_type'] == 'Renda') & (transactions['category'] == category)]['paid_value'].sum() for category in renda_categories}

    # Create the second bar for 'Renda' categories
    bottom = 0
    for category in renda_categories:
        category_sum = renda_sums_grouped[category]
        p = ax.bar(1, category_sum, 0.35, bottom=bottom, label=category)
        bottom += category_sum

        # Add the values inside the bars
        for rect in p:
            height = rect.get_height()
            ax.text(rect.get_x() + rect.get_width() / 2., bottom,
                    'R$ {:.0f}'.format(height),
                    ha='center', va='bottom')

    ax.set_title('Valores totais por categoria e tipo de transação')
    ax.set_xticks([0, 1])
    ax.set_xticklabels(['Despesa, Ativo, Passivo', 'Renda'])
    ax.legend()

    # Format y axis as currency
    formatter = ticker.FuncFormatter(lambda x, pos: 'R$ {:.0f}'.format(x))
    ax.yaxis.set_major_formatter(formatter)

    plt.show()

    # Ensure the directory exists
    os.makedirs('app/static/images', exist_ok=True)

    plt.savefig('app/static/images/transaction_counts_by_category_and_type2.png')

def get_bar_label_balance(transactions):
    fig, ax = plt.subplots()

    # Calculate sums for each group
    money_out = transactions[transactions['transaction_type'].isin(['Despesa', 'Ativo', 'Passivo'])]['paid_value'].sum()
    money_in = transactions[transactions['transaction_type'] == 'Renda']['paid_value'].sum()

    # Calculate the balance
    balance = money_in - money_out

    # Create the bar for 'Money Out'
    p = ax.bar(0, money_out, 0.35, label='Gasto', color='red')

    # Add the value inside the bar
    for rect in p:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width() / 2., height,
                'R$ {:.0f}'.format(height),
                ha='center', va='bottom')

    # Create the bar for 'Balance'
    p = ax.bar(0, balance, 0.35, bottom=money_out, label='Saldo', color='green')

    # Add the value inside the bar
    for rect in p:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width() / 2., money_out + height,
                'R$ {:.0f}'.format(money_out + height),
                ha='center', va='bottom')

    ax.set_title('Saldo')
    ax.set_xticks([0])
    ax.set_xticklabels([''])
    ax.legend()

    # Format y axis as currency
    formatter = ticker.FuncFormatter(lambda x, pos: 'R$ {:.0f}'.format(x))
    ax.yaxis.set_major_formatter(formatter)

    plt.show()

    # Ensure the directory exists
    os.makedirs('app/static/images', exist_ok=True)

    plt.savefig('app/static/images/balance.png')

def save_pie_chart(transaction_type, transactions):
    fig, ax = plt.subplots(figsize=(6, 3), subplot_kw=dict(aspect="equal"))

    # Filter transactions by the specified transaction type
    filtered_transactions = transactions[transactions['transaction_type'] == transaction_type]

    # Get the total paid_value for each category
    category_totals = filtered_transactions.groupby('category')['paid_value'].sum()

    data = category_totals.values
    categories = category_totals.index

    def func(pct, allvals):
        absolute = int(np.round(pct/100.*np.sum(allvals)))
        return f"{pct:.1f}%\n(R$ {absolute:d})"

    wedges, texts, autotexts = ax.pie(data, autopct=lambda pct: func(pct, data),
                                      textprops=dict(color="w"))

    ax.legend(wedges, categories,
              title="Categories",
              loc="center left",
              bbox_to_anchor=(1, 0, 0.5, 1))

    plt.setp(autotexts, size=8, weight="bold")

    ax.set_title(f"Composição de transações ({transaction_type})")

    # Ensure the directory exists
    os.makedirs('app/static/images', exist_ok=True)

    plt.savefig(f'app/static/images/{transaction_type}_pie_composition.png')

    plt.close(fig)  # Close the figure