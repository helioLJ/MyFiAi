from . import db
from .transaction import Transaction

class Asset(Transaction):
    # No need to define fields here, they are inherited from Transaction

    def __repr__(self):
        return f'<Asset {self.name} - R$ {self.paid_value}>'