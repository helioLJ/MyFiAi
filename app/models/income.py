from . import db
from .transaction import Transaction

class Income(Transaction):
    # No need to define fields here, they are inherited from Transaction

    def __repr__(self):
        return f'<Income {self.name} - R$ {self.paid_value}>'