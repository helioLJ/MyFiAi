// Elements
var transactionTypeSelect = document.getElementById('transaction_type_select');
var transactionForm = document.getElementById('transactionForm');
var isProjectedCheckbox = document.getElementById('isProjected');
var openAddModalButton = document.getElementById('openAddModalButton');
var closeAddModalButton = document.getElementById('closeAddModalButton');
var closeEditModalButton = document.getElementById('closeEditModalButton');
var addTransactionModal = document.getElementById('addTransactionModal');
var editTransactionModal = document.getElementById('editTransactionModal');
var deleteModal = document.getElementById('deleteModal');
var paidValueInput = document.getElementById('paid_value');
var expectedValueInput = document.getElementById('expected_value');
let expectedDateField = document.querySelector("#expected_date");
let paydayField = document.querySelector("#payday");
var transactionName = document.getElementById('add_transaction_name');
const categoryField = document.querySelector("#category");

// Event listeners
document.addEventListener('DOMContentLoaded', setDefaultDates);
document.addEventListener('DOMContentLoaded', setupTransactionTypeField);
document.addEventListener('DOMContentLoaded', changeTransactionTypeBorderColor);
transactionForm.addEventListener('submit', validateForm);
isProjectedCheckbox.addEventListener('change', handleProjectedChange);
openAddModalButton.addEventListener('click', openAddModal);
closeAddModalButton.addEventListener('click', closeAddModal);
closeEditModalButton.addEventListener('click', closeEditModal);

// Functions
function setDefaultDates() {
    let today = new Date().toISOString().slice(0, 10);

    if (!expectedDateField.value) {
        expectedDateField.value = today;
    }

    if (!paydayField.value) {
        paydayField.value = today;
    }
}

function validateForm(event) {
    if (!transactionName || !transactionTypeSelect || !expectedValueInput || !paidValueInput) {
        console.log(transactionName, transactionTypeSelect, expectedValueInput, paidValueInput)
        event.preventDefault();
        alert('Please fill out all fields.');
    }
}

function setupTransactionTypeField() {
    const categories = {
        "Renda": ["", "Salário", "Freelance", "Renda Extra", "Aluguel de Propriedades", "Dividendos de Investimentos", "Prêmios e Bônus", "Pensão", "Vendas de Ativos", "Consultoria", "Comissões", "Juros de Empréstimos"],
        "Despesa": ["", "Aluguel/Moradia", "Alimentação", "Transporte", "Saúde", "Educação", "Entretenimento", "Utilidades (água, eletricidade, gás)", "Telefonia/Internet", "Seguros", "Impostos", "Roupas e Acessórios", "Doações", "Viagens", "Manutenção do Veículo", "Restaurantes", "Manutenção Residencial", "Segurança Residencial", "Serviços de Streaming", "Material de Escritório", "Cuidados com Animais de Estimação", "Beleza e Cuidados Pessoais", "Despesas Bancárias", "Educação Continuada", "Equipamentos Eletrônicos", "Hobbies e Passatempos", "Crianças (Despesas relacionadas a filhos)", "Saúde e Bem-Estar", "Assinaturas de Revistas/Jornais", "Taxas de Associações/Clubes", "Despesas de Emergência"],
        "Ativo": ["", "Conta Corrente", "Conta Poupança", "Investimentos em Ações", "Fundos de Investimento", "Títulos Públicos", "Imóveis", "Veículos", "Ouro e Metais Preciosos", "Empresas Próprias", "Recebíveis", "Criptomoedas", "Arte e Colecionáveis", "Propriedade Intelectual", "Empréstimos concedidos", "Patentes"],
        "Passivo": ["", "Empréstimos Pessoais", "Financiamento Imobiliário", "Financiamento de Veículos", "Cartões de Crédito", "Dívidas Estudantis", "Empréstimos Empresariais", "Linhas de Crédito", "Contas a Pagar", "Impostos a Pagar", "Hipotecas", "Leasing", "Dívidas Médicas", "Empréstimos a Familiares", "Dívidas de Cartões de Loja", "Outros Financiamentos"]
    };

    transactionTypeSelect.addEventListener('change', function() {
        populateCategoryField(transactionTypeSelect, categoryField, categories);
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

function handleProjectedChange() {
    paydayField.disabled = this.checked;
    paidValueInput.disabled = this.checked;

    if (this.checked) {
        paydayField.value = null;
        paidValueInput.value = 0;
    } else {
        paydayField.value = new Date().toISOString().slice(0, 10);
    }
}

function openAddModal() {
    addTransactionModal.classList.remove('hidden');
}

function closeAddModal() {
    addTransactionModal.classList.add('hidden');
}

function closeEditModal() {
    editTransactionModal.classList.add('hidden');
}

function openEditModal(id, name, transactionType, category, details, expectedDate, payday, recurrence, expectedValue, paidValue) {
    editTransactionModal.classList.remove('hidden');
    document.getElementById('editTransactionForm').action = '/edit/' + id;
    document.getElementById('edit_name').value = name;
    document.getElementById('edit_transaction_type').value = transactionType;
    document.getElementById('edit_category').value = category;
    document.getElementById('edit_details').value = details;
    expectedDate = expectedDate.split(' ')[0];
    payday = payday.split(' ')[0];
    document.getElementById('edit_expected_date').value = expectedDate;
    document.getElementById('edit_payday').value = payday;
    document.getElementById('edit_recurrence').value = recurrence;
    document.getElementById('edit_expected_value').value = expectedValue;
    document.getElementById('edit_paid_value').value = paidValue;
}

function openDeleteModal(id) {
    document.getElementById('deleteModal').classList.remove('hidden');
    document.querySelector('#deleteModal a').href = '/delete/' + id;
}

function closeDeleteModal() {
    document.getElementById('deleteModal').classList.add('hidden');
}

function changeTransactionTypeBorderColor() {
    transactionTypeSelect.addEventListener('change', function() {
        if (this.value === 'Renda') {
            paidValueInput.style.borderColor = '#22c55e';
            expectedValueInput.style.borderColor = '#22c55e';
        } if (this.value === 'Despesa') {
            paidValueInput.style.borderColor = '#ef4444';
            expectedValueInput.style.borderColor = '#ef4444';
        } if (this.value === 'Ativo') {
            paidValueInput.style.borderColor = '#3b82f6';
            expectedValueInput.style.borderColor = '#3b82f6';
        } if (this.value === 'Passivo') {
            paidValueInput.style.borderColor = '#f97316';
            expectedValueInput.style.borderColor = '#f97316';
        }
    });
}