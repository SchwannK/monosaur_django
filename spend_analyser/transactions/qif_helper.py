"""
    QIF specific subclass of parser.Parser.
    Tries to fetch transactions from a QIF file.
    As a side effect, all payee+memo strings that are not yet in our database 
    are saved for later categorization on an admin page.
"""
from builtins import int
from datetime import datetime
import sys

from django.core.files.base import ContentFile

from monosaur.utils import string_utils
from spend_analyser.models import Transaction, Session
from spend_analyser.transactions import transaction_handler

from .parser import Parser


class QifHelper(Parser):
    
    @classmethod
    def read_transactions(self, file, session):
        qif_transactions = parseQif(file)
        transactions = []
    
        for qif_transaction in qif_transactions:
            category = transaction_handler.get_category(qif_transaction.payee)
            subscription = transaction_handler.get_subscription(qif_transaction.payee)
            name = string_utils.to_empty(qif_transaction.payee) + ' ' + string_utils.to_empty(qif_transaction.memo)
            transactions.append(Transaction(name = name.strip(),\
                                            amount = qif_transaction.amount, date = qif_transaction.date, category = category, subscription = subscription, session = session))
        return transactions
        
    def __str__(self):
        return "QifHelper"
    
class QifItem:
    def __init__(self):
        self.order = ['date', 'amount', 'cleared', 'num', 'payee', 'memo', 'address', 'category', 'categoryInSplit', 'memoInSplit', 'amountOfSplit']
        self.date = None
        self.amount = None
#         self.cleared = None
#         self.num = None
        self.payee = None
        self.memo = None
#         self.address = None
#         self.category = None
#         self.categoryInSplit = None
#         self.memoInSplit = None
#         self.amountOfSplit = None

    def show(self):
        pass
    
    def __repr__(self):
        titles = ','.join(self.order)
        tmpstring = ','.join( [str(self.__dict__[field]) for field in self.order] )
        tmpstring = tmpstring.replace('None', '')
        return titles + "," + tmpstring

    def dataString(self):
        """
        Returns the data of this QIF without a header row
        """
        tmpstring = ','.join( [str(self.__dict__[field]) for field in self.order] )
        tmpstring = tmpstring.replace('None', '')
        return tmpstring
    
def parseQif(infile):
    """
    Parse a qif file and return a list of entries.
    infile should be open file-like object (supporting readline() ).
    """

    inItem = False

    items = []
    curItem = QifItem()
    
    while True:
        line = str(infile.readline(),'utf-8').strip()

        if line == '':
            break
        
        if line[0] == '\n': # blank line
            pass
        elif line[0] == '^': # end of item
            # save the item
            items.append(curItem)
            curItem = QifItem()
        elif line[0] == 'D':
            curItem.date = datetime.strptime(line[1:], "%d/%m/%Y").date()
        elif line[0] == 'T':
            curItem.amount = line[1:]
#         elif line[0] == 'C':
#             curItem.cleared = line[1:]
        elif line[0] == 'P':
            curItem.payee = line[1:]
        elif line[0] == 'M':
            curItem.memo = line[1:]
#         elif line[0] == 'A':
#             curItem.address = line[1:]
#         elif line[0] == 'L':
#             curItem.category = line[1:]
#         elif line[0] == 'S':
#             try:
#                 curItem.categoryInSplit.append(";" + line[1:])
#             except AttributeError:
#                 curItem.categoryInSplit = line[1:]
#         elif line[0] == 'E':
#             try:
#                 curItem.memoInSplit.append(";" + line[1:])
#             except AttributeError:
#                 curItem.memoInSplit = line[1:]
#         elif line[0] == '$':
#             try:
#                 curItem.amountInSplit.append(";" + line[1:])
#             except AttributeError:
#                 curItem.amountInSplit = line[1:]
        else:
            # don't recognise this line; ignore it
            print("Skipping unknown line: " + line[1:])
    return items