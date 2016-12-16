"""
    Database manipulating/querying methods related to transactions
"""
from datetime import datetime

from django.db.utils import IntegrityError
from django.utils import timezone

from monosaur.models import Category, Company
from spend_analyser.models import Transaction
from spend_analyser.transactions.qif_helper import QifHelper
from subscriptions.models import Subscription
from .ofx_helper import OfxHelper

from .constants import DEFAULT_TRANSACTION_CATEGORY


# Returns the number of transactions read from the file 
# and the number of those transactions that were actually saved 
# (ones that didn't violate any uniqueness constraints, a.k.a. 'new transactions'
def process_file(file, session, success_files_out, error_files_out):
    read_count = 0
    save_count = 0
    # add new parsers here
    # they are going to be used in the order in which you specify them
    # if one fails, the next one is tried
    # if all parsers fail, uncomment the error handling in the try_parser method to see what's going on
    parsers = [OfxHelper(), QifHelper()]

    for parser in parsers:
        transactions = read_transactions(parser, file, session)
        
        if transactions and len(transactions) > 0:
            read_count = len(transactions)
            break

    if read_count > 0:
        save_count = save(transactions)
        success_files_out.append(str(file))
    else:
        error_files_out.append(str(file))
    return read_count, save_count

# try reading the file with the specified parser
# if the parser actually matches the file, the transactions will be returned
# otherwise and empty array is returned
def read_transactions(parser, file, session):
    transactions = []
    try:
        transactions = parser.read_transactions(file, session)
                
        # in the above read_transactions method, all new companies were inserted to Company
        # let's export it so we don't lose them on the next db reset
        Company.save_to_fixture()
    except Exception as e:
        print("==== error parsing with " + str(parser) + ": " + str(e))
#       traceback.print_exc()
#       raise e
    return transactions


# See if the reference can be found in the Categories db and return the entry
# If it's not found, the reference is marked for later categorisation
def get_category(reference):
    # Not the best solution as it's specific to SQLite. And the point of querysets is to be abstracted from the concrete db implementation. But it's ok for now
    companies = Company.objects.raw("SELECT * FROM monosaur_company where %s LIKE '%%' || reference || '%%'", [reference])[:1]
    category = None
    
    if companies and companies[0].category:
        category = companies[0].category
        
    if category is None:
        try:
            if not companies:
                # mark the reference for later categorisation
                Company(reference=reference).save()
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
    older_than = timezone.now() - datetime.timedelta(days=1)
    delete_count, breakdown = Transaction.objects.filter(session__last_read__lt=older_than).delete()
    print("Clearing transactions older than 1 day: " + str(delete_count))
    return delete_count

def delete_all_entries():
    delete_count, breakdown = Transaction.objects.all().delete()
    print("Clearing transactions: " + str(delete_count))
    return delete_count
