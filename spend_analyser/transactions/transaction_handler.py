"""
    Database manipulating/querying methods related to transactions
"""
from datetime import datetime, timedelta

from django.db.utils import IntegrityError

from monosaur.models import Category, Company, FixtureCompany
from spend_analyser.models import Transaction
from subscriptions.models import Subscription

from .constants import DEFAULT_TRANSACTION_CATEGORY


# See if the reference can be found in the Categories db and return the entry
# If it's not found, the payee is marked for later categorization
def get_category(reference):
    # Not the best solution as it's specific to SQLite. And the point of querysets is to be abstracted from the concrete db implementation. But it's ok for now
    companies = Company.objects.raw("SELECT * FROM monosaur_company where %s LIKE '%%' || reference || '%%'", [reference])[:1]
    category = None
    
    if companies and companies[0].category:
        category = companies[0].category
        
    if category is None:
        try:
            if companies:
                name = companies[0].name
            else:
                name = None
            FixtureCompany(reference=reference, name=name).save()
        except:
            pass
        return Category.objects.get(name=DEFAULT_TRANSACTION_CATEGORY)
    else:
        return category

# See if the reference can be found in the Subscription db and return the entry
def get_subscription(reference):
    # Not the best solution as it's specific to SQLite. And the point of querysets is to be abstracted from the concrete db implementation. But it's ok for now
    subscriptions = Subscription.objects.raw("SELECT * FROM subscriptions_subscription where %s LIKE '%%' || reference || '%%'", [reference])[:1]
    if subscriptions:
        return subscriptions[0]
    else:
        return None

# Save an array of Transaction models, on uniqueness constraint violation->continue
# Returns the number of successfully saved (unique) transactions
def save(transactions):
    row_count = 0
    for transaction in transactions:
        try:
            transaction.save(force_insert=False, force_update=False)
            
            if transaction.pk:
                row_count = row_count + 1
        except IntegrityError as e:
            if "UNIQUE" in str(e) :
                print("unique constraint failed: " + transaction.name + " " + str(transaction.amount) + " " + str(transaction.date))
            else:
                raise e
    return row_count
                
def delete_old_entries():
    delete_count = delete_entries(datetime.now() - timedelta(days=1))
    print("Clearing transactions older than 1 day: " + str(delete_count))
    return delete_count

def delete_all_entries():
    delete_count = delete_entries(datetime.now())
    print("Clearing transactions: " + str(delete_count))
    return delete_count

def delete_entries(older_than):
    delete_count, breakdown = Transaction.objects.filter(session__last_read__lt=older_than).delete()
    return delete_count
