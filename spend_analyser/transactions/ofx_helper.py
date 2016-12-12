from ofxparse import OfxParser

from monosaur.string_utils import empty
from spend_analyser.models import Transaction
from spend_analyser.transactions import transaction_handler

from .parser import Parser


class OfxHelper(Parser):

    @classmethod
    def read_transactions(self, file, session):
        ofx_transactions = OfxParser.parse(file).account.statement.transactions
        transactions = []
    
        for ofx_transaction in ofx_transactions:
            category = transaction_handler.get_category(ofx_transaction.payee)
            subscription = transaction_handler.get_subscription(ofx_transaction.payee)
            name = empty(ofx_transaction.payee) + ' ' + empty(ofx_transaction.memo)
            transactions.append(Transaction(name = name.strip(), amount = ofx_transaction.amount, date = ofx_transaction.date, category = category, subscription = subscription, session = session))
            
        return transactions

    def __str__(self):
        return "OfxHelper"