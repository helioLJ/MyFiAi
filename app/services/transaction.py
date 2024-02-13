from datetime import datetime

from flask import request, url_for
from openai import OpenAI

from ..models import Transaction, db

client = OpenAI()

def get_month_transactions():
    page = request.args.get('page', 1, type=int)
    per_page = 30  # Change this to the number of items you want per page
    month = request.args.get('month', datetime.now().month, type=int)
    if month is None:
        month = datetime.now().month
    transactions = Transaction.query.filter(db.extract('month', Transaction.payday) == month)
    paginated_transactions = transactions.paginate(page=page, per_page=per_page, error_out=False)
    next_url = url_for('index', page=paginated_transactions.next_num, month=month) if paginated_transactions.has_next else None
    prev_url = url_for('index', page=paginated_transactions.prev_num, month=month) if paginated_transactions.has_prev else None
    return paginated_transactions.items, next_url, prev_url, month

def insert_transaction():
    if request.method == 'POST':
        name = request.form.get('name')
        category = request.form.get('category')
        transaction_type = request.form.get('transaction_type')
        details = request.form.get('details')
        expected_date = datetime.strptime(request.form.get('expected_date'), '%Y-%m-%d')
        expected_date_str = request.form.get('payday')
        if expected_date_str is not None:
            expected_date = datetime.strptime(expected_date_str, '%Y-%m-%d')
        else:
            expected_date = None
        payday_str = request.form.get('payday')
        if payday_str is not None:
            payday = datetime.strptime(payday_str, '%Y-%m-%d')
        else:
            payday = None
        recurrence = request.form.get('recurrence')
        expected_value = float(request.form.get('expected_value'))
        paid_value = float(request.form.get('paid_value'))

        if not category:
            category = define_category(transaction_type, name)

        new_transaction = Transaction(
            name=name,
            category=category,
            details=details,
            expected_date=expected_date,
            payday=payday,
            recurrence=recurrence,
            expected_value=expected_value,
            paid_value=paid_value,
            transaction_type=transaction_type
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

             Retorn apenas o nome da categoria.
             
             Exemplo de resposta bem sucedida: Viagens
             
             Lista: {lista}

            """},
            {"role": "user", "content": f"{transaction_name}"}
        ]
    )

    return completion.choices[0].message.content