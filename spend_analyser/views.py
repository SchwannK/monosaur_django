from django.shortcuts import render
from ofxparse import OfxParser
from .models import Transaction, Category, Company
from subscription_list.models import Subscription
import io

# Create your views here.

def spend_analyser(request):
    if request.method == "POST":
        add_transactions_to_db(request.FILES['ofx_file'].file)

    transactions = Transaction.objects.order_by('-date')
    return render(request, 'spend_analyser/transaction_list.html', {'transactions': transactions})

def add_transactions_to_db(ofx_file):

    try:
        ofx = OfxParser.parse(ofx_file)

        for transaction in ofx.account.statement.transactions:

            transaction_cat = "Other"
            for company in Company.objects.all():
                if company.reference in transaction.payee:
                    transaction_cat = company.category

            subscription_name = "No"
            for subscription in Subscription.objects.all():
                if subscription.transaction_reference in transaction.payee:
                    print("yes!")
                    subscription_name = subscription.subscription_name

            newTransaction = Transaction.objects.get_or_create(name=transaction.payee, amount=transaction.amount, date=transaction.date, category=transaction_cat, subscription=subscription_name)

    except:
        print("File not valid!")
