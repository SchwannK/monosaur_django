from ofxparse import OfxParser

from spend_analyser.models import Transaction

from .parser import Parser
from .transactions import get_category, get_subscription


class OfxHelper(Parser):

    @classmethod
    def read_transactions(self, file, session_id):
        ofx_transactions = OfxParser.parse(file).account.statement.transactions
        transactions = []
    
        for ofx_transaction in ofx_transactions:
            category = get_category(ofx_transaction.payee)
            subscription = get_subscription(ofx_transaction.payee)
            transactions.append(Transaction(name = ofx_transaction.payee, amount = ofx_transaction.amount, date = ofx_transaction.date, category = category, subscription = subscription, user = session_id))
            
        return transactions

