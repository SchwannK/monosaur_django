from abc import ABC, abstractmethod

from monosaur.utils import string_utils
from spend_analyser.models import Transaction
from spend_analyser.transactions import transaction_handler


class Parser(ABC):
    
    @abstractmethod
    def read_transactions(self, file, session_id):
        pass
    
    def get_transaction(self, payee, memo, amount, date, session):
        reference = ''
        if not string_utils.is_empty(payee):
            reference = payee.strip()
        if not string_utils.is_empty(memo):
            reference += ' ' + memo
        category = transaction_handler.get_category(reference)
        subscription = transaction_handler.get_subscription(reference)
        return Transaction(reference=reference, \
                                        amount=amount, date=date, category=category, subscription=subscription, session=session)