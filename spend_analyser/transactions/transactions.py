import traceback

from spend_analyser.models import Transaction, Category, Company
from subscription_list.models import Subscription

from .constants import *


def save_transactions(transactions, session_id):
    try:
        for transaction in transactions:
            category = get_category(transaction)
            subscription = get_subscription(transaction)
            Transaction.objects.get_or_create(name=transaction.payee, amount=transaction.amount, date=transaction.date, category=category, subscription=subscription, user=session_id)
    except Exception as e:
        print("transaction: " + str(e))
        traceback.print_exc()

def get_category(transaction):
    # Not the best solution as it's specific to SQLite. And the point of querysets is to be abstracted from the concrete db implementation. But it's ok for now
    companies = Company.objects.raw("SELECT * FROM spend_analyser_company where %s LIKE '%%' || reference || '%%'", [transaction.payee])[:1]
    if companies:
        return companies[0].category
    else:
        return Category.objects.get(name = DEFAULT_TRANSACTION_CATEGORY)

def get_subscription(transaction):
    # Not the best solution as it's specific to SQLite. And the point of querysets is to be abstracted from the concrete db implementation. But it's ok for now
    subscriptions = Subscription.objects.raw("SELECT * FROM subscription_list_subscription where %s LIKE '%%' || transaction_reference || '%%'", [transaction.payee])[:1]
    if subscriptions:
        return subscriptions[0]
    else:
        return None
    