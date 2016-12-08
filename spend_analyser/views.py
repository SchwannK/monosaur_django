from django.shortcuts import render
from ofxparse import OfxParser
from .models import Transaction, Category, Company
from subscription_list.models import Subscription
import io, operator

DEFAULT_TRANSACTION_CAT = "Other"
DEFAULT_SUBSCRIPTION_NAME = "-"

# Create your views here.

def spend_analyser(request):
    if request.method == "POST":
        add_transactions_to_db(request.FILES['ofx_file'].file)

    chart_data = process_data()
    chart_labels = list(list(zip(*chart_data))[0])
    chart_values = list(list(zip(*chart_data))[1])

    transactions = Transaction.objects.order_by('-date')
    return render(request, 'spend_analyser/transaction_list.html', {'transactions': transactions, 'chart_values': chart_values, 'chart_labels': chart_labels,})

def add_transactions_to_db(ofx_file):

    try:
        ofx = OfxParser.parse(ofx_file)

        for transaction in ofx.account.statement.transactions:

            try:
                transaction_cat = DEFAULT_TRANSACTION_CAT
                for company in Company.objects.all():
                    if company.reference.upper() in transaction.payee:
                        transaction_cat = company.category

                subscription_name = DEFAULT_SUBSCRIPTION_NAME
                for subscription in Subscription.objects.all():
                    if subscription.transaction_reference.upper() in transaction.payee:
                        subscription_name = subscription.subscription_name

                newTransaction = Transaction.objects.get_or_create(name=transaction.payee, amount=transaction.amount, date=transaction.date, category=transaction_cat, subscription=subscription_name)
            except:
                print("Transaction error.")
    except:
        print("File not valid!")

def process_data():

    category_totals = {} # Initialise dictionary which will store totals for each category
    overall_total = 0

    for category in Category.objects.all():
        category_totals[category.name] = 0      # Initialise all totals to 0

    for transaction in Transaction.objects.all():
        category_totals[transaction.category] -= transaction.amount # minus to invert sign
        overall_total -= transaction.amount

    other_total = category_totals.pop(DEFAULT_TRANSACTION_CAT)

    sorted_categories = sorted(category_totals, key=category_totals.get, reverse=True)[:4]
    top_total = 0
    for top_cat in sorted_categories:
        top_total += category_totals[top_cat]

    sorted_categories.append(DEFAULT_TRANSACTION_CAT)
    category_totals[DEFAULT_TRANSACTION_CAT] = overall_total - top_total

    chart_data = [(cat, round(category_totals[cat],2)) for cat in sorted_categories]

    # for key, value in chart_data:
    #    print("%s: %d" % (key, value))

    return chart_data
