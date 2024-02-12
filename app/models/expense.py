from . import db
from .transaction import Transaction

class Expense(Transaction):
    # No need to define fields here, they are inherited from Transaction

    def __repr__(self):
        return f'<Expense {self.name} - R$ {self.paid_value}>'