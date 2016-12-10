from ofxparse import OfxParser
from .transactions import get_category, get_subscription
from spend_analyser.models import Transaction


def read_transactions(ofx_file, session_id):
    ofx_transactions = OfxParser.parse(ofx_file).account.statement.transactions
    transactions = []
    
    for ofx_transaction in ofx_transactions:
            category = get_category(ofx_transaction.payee)
            subscription = get_subscription(ofx_transaction.payee)
            transactions.append(Transaction(name = ofx_transaction.payee, amount = ofx_transaction.amount, date = ofx_transaction.date, category = category, subscription = subscription, user = session_id))
            
    return transactions
#             Transaction.objects.get_or_create(name=transaction.payee, amount=transaction.amount, date=transaction.date, category=category, subscription=subscription, user=session_id)

