"""
    OFX specific subclass of parser.Parser.
    Tries to fetch transactions from an OFX file.
    As a side effect, all payee+memo strings that are not yet in our database 
    are saved for later categorization on an admin page.
"""
from ofxparse import OfxParser

from monosaur.utils import string_utils
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
            name = string_utils.to_empty(ofx_transaction.payee) + ' ' + string_utils.to_empty(ofx_transaction.memo)
            transactions.append(Transaction(name=name.strip(), amount=ofx_transaction.amount, date=ofx_transaction.date, category=category, subscription=subscription, session=session))
            
        return transactions

    def __str__(self):
        return "OfxHelper"
