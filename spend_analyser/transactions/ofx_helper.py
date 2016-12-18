"""
    OFX specific subclass of parser.Parser.
    Tries to fetch transactions from an OFX file.
    As a side effect, all payee+memo strings that are not yet in our database 
    are saved for later categorization on an admin page.
"""
from ofxparse import OfxParser

from .parser import Parser


class OfxHelper(Parser):

    @classmethod
    def read_transactions(self, file, session):
        ofx_transactions = OfxParser.parse(file).account.statement.transactions
        transactions = []
    
        for ofx_transaction in ofx_transactions:
            transactions.append(self.get_transaction(self, ofx_transaction.payee, ofx_transaction.memo, ofx_transaction.amount, ofx_transaction.date, session))
            
        return transactions

    def __str__(self):
        return "OfxHelper"
