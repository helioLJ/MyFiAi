from datetime import datetime

from flask import request, url_for, flash, abort
from flask_login import current_user
from sqlalchemy import desc, extract
from openai import OpenAI
from markdown import markdown

from ..models import User, Transaction, Insight, db

client = OpenAI()

def get_page_and_per_page():
    page = request.args.get('page', 1, type=int)
    per_page = 30  # Change this to the number of items you want per page
    return page, per_page

def get_month():
    month = request.args.get('month', datetime.now().month, type=int)
    if month is None:
        month = datetime.now().month
    return month

def get_sort():
    return request.args.get('sort', 'expected_date', type=str)

def get_transaction_type():
    return request.args.get('transaction_type', None, type=str)

def filter_transactions_by_month(month):
    user_id = current_user.get_id()
    return Transaction.query.filter(db.extract('month', Transaction.expected_date) == month, Transaction.user_id == user_id)

def filter_transactions_by_type(transactions, transaction_type):
    if transaction_type is not None:
        transactions = transactions.filter(Transaction.transaction_type == transaction_type)
    return transactions

def sort_transactions(transactions, sort):
    sort_options = {
        'transaction_type': lambda: transactions.order_by(desc(Transaction.transaction_type)),
        'payday': lambda: transactions.order_by(desc(Transaction.payday)),
        'expected_date': lambda: transactions.order_by(Transaction.expected_date),
        'paid_value': lambda: transactions.order_by(desc(Transaction.paid_value)),
        'expected_value': lambda: transactions.order_by(desc(Transaction.expected_value)),
    }
    return sort_options.get(sort, lambda: transactions)()

def get_paginated_transactions(transactions, page, per_page):
    return transactions.paginate(page=page, per_page=per_page, error_out=False)

def get_balance_data(month):
    user_id = current_user.get_id()
    types = ['Renda', 'Despesa', 'Ativo', 'Passivo']
    data = {}

    for t in types:
        current_balance = db.session.query(db.func.sum(Transaction.paid_value)).filter(
            Transaction.transaction_type == t, 
            Transaction.user_id == user_id,
            extract('month', Transaction.payday) == month
        ).scalar() or 0

        projected_balance = db.session.query(db.func.sum(Transaction.expected_value)).filter(
            Transaction.transaction_type == t, 
            Transaction.user_id == user_id,
            extract('month', Transaction.expected_date) == month
        ).scalar() or 0

        data[t] = {'Valor Atual': current_balance, 'Valor Projetado': projected_balance}

    total_current_balance = data['Renda']['Valor Atual'] - data['Despesa']['Valor Atual'] - data['Ativo']['Valor Atual'] - data['Passivo']['Valor Atual']
    total_projected_balance = data['Renda']['Valor Projetado'] - data['Despesa']['Valor Projetado'] - data['Ativo']['Valor Projetado'] - data['Passivo']['Valor Projetado']

    data['Saldo'] = {'Saldo Atual': total_current_balance, 'Saldo Projetado': total_projected_balance}
    
    data['Despesa']['Valor Atual'] = -data['Despesa']['Valor Atual']
    data['Despesa']['Valor Projetado'] = -data['Despesa']['Valor Projetado']

    data['Ativo']['Valor Atual'] = -data['Ativo']['Valor Atual']
    data['Ativo']['Valor Projetado'] = -data['Ativo']['Valor Projetado']

    data['Passivo']['Valor Atual'] = -data['Passivo']['Valor Atual']
    data['Passivo']['Valor Projetado'] = -data['Passivo']['Valor Projetado']
    return data

def get_month_transactions():
    page, per_page = get_page_and_per_page()
    month = get_month()
    sort = get_sort()
    transaction_type = get_transaction_type()
    transactions = filter_transactions_by_month(month)
    transactions = filter_transactions_by_type(transactions, transaction_type)
    transactions = sort_transactions(transactions, sort)
    paginated_transactions = get_paginated_transactions(transactions, page, per_page)
    next_url = url_for('index', page=paginated_transactions.next_num, month=month, sort=sort) if paginated_transactions.has_next else None
    prev_url = url_for('index', page=paginated_transactions.prev_num, month=month, sort=sort) if paginated_transactions.has_prev else None
    balance_data = get_balance_data(month)
    insights, can_generate_insight = give_insights(current_user.get_id(), month)
    return {
        'transactions': paginated_transactions.items,
        'next_url': next_url,
        'prev_url': prev_url,
        'current_month': month,
        'balance_data': balance_data,
        'insights': markdown(insights),
        'can_generate_insight': can_generate_insight,
    }

def give_insights(user_id, month):
    insight = Insight.query.filter(Insight.user_id==user_id, Insight.month==month).first()
    current_year = datetime.now().year
    existing_insight = insight and insight.created_at.year == current_year
    user = User.query.get(user_id)
    can_generate_insight = user.is_premium or not existing_insight
    text = insight.text if existing_insight else "Adicione no mínimo 10 transações para gerar insights."
    return text, can_generate_insight
    
def generate_insight():
    month = get_month()
    balanco = get_balance_data(month)

    messages = [
                {"role": "system", "content": f"""
                    Você vai receber uma dicionário em Python com informações sobre balanço mensal de uma pessoa.

                    Despesas, Ativos e Passivos significa dinheiro que saiu.
                    Renda significa dinheiro que entrou.

                    Gere insights sobre o balanço financeiro do usuário, como por exemplo, se ele está gastando mais do que ganha, se está economizando, se está investindo, se está endividado, etc.

                    E traga soluções para os problemas encontrados.
                    Se comunique como se estivesse falando com o usuário dono do balanço.

                    Retorne o texto dividido com tags HTML.
                """},
                {"role": "user", "content": f"{balanco}"}
            ]
    current_year = datetime.now().year

    existing_insight = insight and insight.created_at.year == current_year

    if existing_insight:
        # Obtém o usuário
        user = User.query.get(current_user.get_id())
        if user.is_premium: # Coloquei NOT para não ficar fazendo chamadas

            # Se o usuário for premium, gera outro insight
            completion = client.chat.completions.create(
                model="gpt-3.5-turbo",
                temperature=0,
                messages=messages
            )

            result = completion.choices[0].message.content

            # Atualiza o insight existente
            insight.text = result
            insight.updated_at = datetime.now()

            db.session.commit()

            return result
        else:
            # Se o usuário não for premium, retorna o insight atual
            return insight.text
    else:
        # Se não existir um insight com o mesmo mês e ano, cria um novo
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            temperature=0,
            messages=messages
        )

        result = completion.choices[0].message.content

        # Cria uma nova instância de Insight
        insight = Insight(
            month=month,
            text=result,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            user_id=current_user.get_id()
        )

        # Adiciona a instância de Insight à sessão do banco de balanco
        db.session.add(insight)

        # Commit as alterações na sessão do banco de dados
        db.session.commit()

        return result

def insert_transaction():
    if request.method == 'POST':
        name = request.form.get('name')
        category = request.form.get('category')
        transaction_type = request.form.get('transaction_type')
        details = request.form.get('details')

        expected_date = datetime.strptime(request.form.get('expected_date'), '%Y-%m-%d')
        expected_date_str = request.form.get('expected_date')
        if expected_date_str is not None:
            expected_date = datetime.strptime(expected_date_str, '%Y-%m-%d')
        else:
            expected_date = None

        isProjected = request.form.get('isProjected')
        payday = None
        if isProjected is None:
            payday_str = request.form.get('payday')
            if payday_str is not None:
                payday = datetime.strptime(payday_str, '%Y-%m-%d')

        recurrence = request.form.get('recurrence')
        expected_value = float(request.form.get('expected_value'))
        if request.form.get('paid_value') is None:
            paid_value = 0
        else:
            paid_value = float(request.form.get('paid_value'))

        paid_value = abs(paid_value)
        expected_value = abs(expected_value)

        if not category:
            # category = define_category(transaction_type, name)
            category = "IA..."

        new_transaction = Transaction(
            name=name,
            category=category,
            details=details,
            expected_date=expected_date,
            payday=payday,
            recurrence=recurrence,
            expected_value=expected_value,
            paid_value=paid_value,
            transaction_type=transaction_type,
            user_id=current_user.get_id()
        )

        db.session.add(new_transaction)
        db.session.commit()

def define_category(transaction_type, transaction_name):
    renda = """
- Salário
- Freelance
- Renda Extra
- Aluguel de Propriedades
- Dividendos de Investimentos
- Prêmios e Bônus
- Pensão
- Vendas de Ativos
- Consultoria
- Comissões
- Juros de Empréstimos
    """

    despesa = """
- Aluguel/Moradia
- Alimentação
- Transporte
- Saúde
- Educação
- Entretenimento
- Utilidades (água, eletricidade, gás)
- Telefonia/Internet
- Seguros
- Impostos
- Roupas e Acessórios
- Doações
- Viagens
- Manutenção do Veículo
- Restaurantes
- Manutenção Residencial
- Segurança Residencial
- Serviços de Streaming
- Material de Escritório
- Cuidados com Animais de Estimação
- Beleza e Cuidados Pessoais
- Despesas Bancárias
- Educação Continuada
- Equipamentos Eletrônicos
- Hobbies e Passatempos
- Crianças (Despesas relacionadas a filhos)
- Saúde e Bem-Estar
- Assinaturas de Revistas/Jornais
- Taxas de Associações/Clubes
- Despesas de Emergência
    """

    ativo = """
- Conta Corrente
- Conta Poupança
- Investimentos em Ações
- Fundos de Investimento
- Títulos Públicos
- Imóveis
- Veículos
- Ouro e Metais Preciosos
- Empresas Próprias
- Recebíveis
- Criptomoedas
- Arte e Colecionáveis
- Propriedade Intelectual
- Empréstimos concedidos
- Patentes
    """

    passivo = """
- Empréstimos Pessoais
- Financiamento Imobiliário
- Financiamento de Veículos
- Cartões de Crédito
- Dívidas Estudantis
- Empréstimos Empresariais
- Linhas de Crédito
- Contas a Pagar
- Impostos a Pagar
- Hipotecas
- Leasing
- Dívidas Médicas
- Empréstimos a Familiares
- Dívidas de Cartões de Loja
- Outros Financiamentos
    """

    lista = None

    if transaction_type == 'Renda':
        lista = renda
    elif transaction_type == 'Despesa':
        lista = despesa
    elif transaction_type == 'Ativo':
        lista = ativo
    elif transaction_type == 'Passivo':
        lista = passivo

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        temperature=0,
        messages=[
            {"role": "system", "content": f"""
             Você vai receber uma transação e uma lista de categorias, escolha a categoria que melhor se encaixa na transação.
             Caso não encontre a categoria desejada, você pode criar uma nova categoria.
             Caso não consiga categorizar a transação, retorne "Outros".

             Retorn apenas o nome da categoria.
             
             Exemplo de resposta bem sucedida: Viagens
             
             Lista: {lista}

            """},
            {"role": "user", "content": f"{transaction_name}"}
        ]
    )

    return completion.choices[0].message.content

def edit_transaction(id):
    transaction = Transaction.query.get_or_404(id)
    if transaction.user_id != current_user.get_id():
        abort(403)  # HTTP status code for "Forbidden"
    if request.method == 'POST':
        transaction.name = request.form['name']
        transaction.transaction_type = request.form['transaction_type']
        transaction.category = request.form['category']
        transaction.details = request.form['details']
        transaction.expected_date = datetime.strptime(request.form['expected_date'], '%Y-%m-%d').date()
        transaction.payday = datetime.strptime(request.form['payday'], '%Y-%m-%d').date()
        transaction.recurrence = request.form['recurrence']
        transaction.expected_value = float(request.form['expected_value'])
        transaction.paid_value = float(request.form['paid_value'])
        db.session.commit()
        flash('Transaction updated successfully!', 'success')

def delete_transaction(id):
    transaction = Transaction.query.get_or_404(id)
    if transaction.user_id != current_user.get_id():
        abort(403)  # HTTP status code for "Forbidden"
    db.session.delete(transaction)
    db.session.commit()
    flash('Transaction deleted successfully!', 'success')