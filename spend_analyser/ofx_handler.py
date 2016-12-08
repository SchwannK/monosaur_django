from ofxparse import OfxParser

from subscription_list.models import Subscription

from .models import Transaction, Category, Company


DEFAULT_TRANSACTION_CAT = "Other"
DEFAULT_SUBSCRIPTION_NAME = "-"

def read_transactions(ofx_file):
    return OfxParser.parse(ofx_file).account.statement.transactions

def save_transactions(transactions, session_id):
    try:
        for transaction in transactions:
            try:
                transaction_cat = DEFAULT_TRANSACTION_CAT
                for company in Company.objects.all():
                    if company.reference.upper() in transaction.payee:
                        transaction_cat = company.category

                subscription_name = DEFAULT_SUBSCRIPTION_NAME
                for subscription in Subscription.objects.all():
                    if subscription.transaction_reference.upper() in transaction.payee:
                        subscription_name = subscription.subscription_name

                newTransaction = Transaction.objects.get_or_create(name=transaction.payee, amount=transaction.amount, date=transaction.date, category=transaction_cat, subscription=subscription_name, user=session_id)
            except Exception as e:
                print("Transaction error: " + str(e))
    except Exception as e:
        print("File not valid: " + str(e))
        
def get_chart():
    category_totals = {}  # Initialise dictionary which will store totals for each category
    overall_total = 0

    for category in Category.objects.all():
        category_totals[category.name] = 0  # Initialise all totals to 0

    for transaction in Transaction.objects.all():
        category_totals[transaction.category] = category_totals.get(transaction.category, 0) - transaction.amount  # minus to invert sign
        overall_total -= transaction.amount

#     other_total = category_totals.pop(DEFAULT_TRANSACTION_CAT)

    sorted_categories = sorted(category_totals, key=category_totals.get, reverse=True)[:4]
    top_total = 0
    for top_cat in sorted_categories:
        top_total += category_totals[top_cat]

    sorted_categories.append(DEFAULT_TRANSACTION_CAT)
    
    if DEFAULT_TRANSACTION_CAT in category_totals:
        category_totals[DEFAULT_TRANSACTION_CAT] = overall_total - top_total

    chart_data = [(cat, round(category_totals.get(cat, 0), 2)) for cat in sorted_categories]

    # for key, value in chart_data:
    #    print("%s: %d" % (key, value))

    return chart_data
