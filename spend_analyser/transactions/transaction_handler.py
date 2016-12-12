from datetime import datetime, timedelta
import traceback

from django.db.utils import IntegrityError

from monosaur.models import Category, Company
from spend_analyser.models import Transaction
from subscriptions.models import Subscription

from .constants import DEFAULT_TRANSACTION_CATEGORY


def get_category(payee):
    # Not the best solution as it's specific to SQLite. And the point of querysets is to be abstracted from the concrete db implementation. But it's ok for now
    companies = Company.objects.raw("SELECT * FROM monosaur_company where %s LIKE '%%' || reference || '%%'", [payee])[:1]
    if companies:
        return companies[0].category
    else:
        return Category.objects.get(name=DEFAULT_TRANSACTION_CATEGORY)

def get_subscription(payee):
    # Not the best solution as it's specific to SQLite. And the point of querysets is to be abstracted from the concrete db implementation. But it's ok for now
    subscriptions = Subscription.objects.raw("SELECT * FROM subscriptions_subscription where %s LIKE '%%' || reference || '%%'", [payee])[:1]
    if subscriptions:
        return subscriptions[0]
    else:
        return None
    
def save(transactions):
        for transaction in transactions:
            try:
                transaction.save(force_insert=False, force_update=False)
            except IntegrityError as e:
                if "UNIQUE" in str(e) :
                    print("unique constraint failed: " + transaction.name + " " + str(transaction.amount) + " " + str(transaction.date))
                else:
                    raise e
                
def delete_old_entries():
    delete_count, breakdown = Transaction.objects.filter(session__last_read__lt=(datetime.now() - timedelta(days=-1))).delete()
    print("Clearing transactions older than 1 day: " + str(delete_count))
    return delete_count
    