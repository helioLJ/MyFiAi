document.addEventListener('DOMContentLoaded', setDefaultDates);
document.getElementById('openModalButton').addEventListener('click', openModal);
document.getElementById('closeModalButton').addEventListener('click', closeModal);
document.getElementById('transactionForm').addEventListener('submit', validateForm);
document.addEventListener('DOMContentLoaded', setupTransactionTypeField);

document.getElementById('isProjected').addEventListener('change', function() {
    let paydayField = document.getElementById('payday');
    paydayField.disabled = this.checked;
    if (this.checked) {
        paydayField.value = '';
    } else {
        paydayField.value = new Date().toISOString().slice(0, 10);
    }
});

function setDefaultDates() {
    let today = new Date().toISOString().slice(0, 10);
    let expectedDateField = document.querySelector("#expected_date");
    let paydayField = document.querySelector("#payday");

    if (!expectedDateField.value) {
        expectedDateField.value = today;
    }

    if (!paydayField.value) {
        paydayField.value = today;
    }
}

function openModal() {
    document.getElementById('transactionModal').classList.remove('hidden');
}

function closeModal() {
    document.getElementById('transactionModal').classList.add('hidden');
}

function validateForm(event) {
    var name = document.getElementById('name').value;
    var transaction_type = document.getElementById('transaction_type').value;
    var expected_value = document.getElementById('expected_value').value;
    var paid_value = document.getElementById('paid_value').value;

    if (!name || !transaction_type || !expected_value || !paid_value) {
        event.preventDefault();
        alert('Please fill out all fields.');
    }
}

function setupTransactionTypeField() {
    const transactionTypeField = document.querySelector("#transaction_type");
    const categoryField = document.querySelector("#category");

    const categories = {
        "Renda": ["", "Salário", "Freelance", "Renda Extra", "Aluguel de Propriedades", "Dividendos de Investimentos", "Prêmios e Bônus", "Pensão", "Vendas de Ativos", "Consultoria", "Comissões", "Juros de Empréstimos"],
        "Despesa": ["", "Aluguel/Moradia", "Alimentação", "Transporte", "Saúde", "Educação", "Entretenimento", "Utilidades (água, eletricidade, gás)", "Telefonia/Internet", "Seguros", "Impostos", "Roupas e Acessórios", "Doações", "Viagens", "Manutenção do Veículo", "Restaurantes", "Manutenção Residencial", "Segurança Residencial", "Serviços de Streaming", "Material de Escritório", "Cuidados com Animais de Estimação", "Beleza e Cuidados Pessoais", "Despesas Bancárias", "Educação Continuada", "Equipamentos Eletrônicos", "Hobbies e Passatempos", "Crianças (Despesas relacionadas a filhos)", "Saúde e Bem-Estar", "Assinaturas de Revistas/Jornais", "Taxas de Associações/Clubes", "Despesas de Emergência"],
        "Ativo": ["", "Conta Corrente", "Conta Poupança", "Investimentos em Ações", "Fundos de Investimento", "Títulos Públicos", "Imóveis", "Veículos", "Ouro e Metais Preciosos", "Empresas Próprias", "Recebíveis", "Criptomoedas", "Arte e Colecionáveis", "Propriedade Intelectual", "Empréstimos concedidos", "Patentes"],
        "Passivo": ["", "Empréstimos Pessoais", "Financiamento Imobiliário", "Financiamento de Veículos", "Cartões de Crédito", "Dívidas Estudantis", "Empréstimos Empresariais", "Linhas de Crédito", "Contas a Pagar", "Impostos a Pagar", "Hipotecas", "Leasing", "Dívidas Médicas", "Empréstimos a Familiares", "Dívidas de Cartões de Loja", "Outros Financiamentos"]
    };

    transactionTypeField.addEventListener('change', function() {
        populateCategoryField(transactionTypeField, categoryField, categories);
    });
}

function populateCategoryField(transactionTypeField, categoryField, categories) {
    const selectedType = transactionTypeField.value;

    // Clear the category field
    categoryField.innerHTML = "";

    // Populate the category field with the appropriate options
    categories[selectedType].forEach((category) => {
        const option = document.createElement("option");
        option.value = category;
        option.text = category;
        categoryField.add(option);
    });
}