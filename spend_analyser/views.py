from django.shortcuts import render
from ofxparse import OfxParser
from .models import Transaction
import io

# Create your views here.

def spend_analyser(request):
    if request.method == "POST":
        add_transactions_to_db(request.FILES['ofx_file'].file)

    transactions = Transaction.objects.order_by('-date')
    return render(request, 'spend_analyser/transaction_list.html', {'transactions': transactions})

def add_transactions_to_db(ofx_file):
    ofx = OfxParser.parse(ofx_file)

    for transaction in ofx.account.statement.transactions:
        newTransaction = Transaction(name=transaction.payee, amount=transaction.amount, date=transaction.date)
        try:
            newTransaction.save()
        except:
            print("There was a problem with the OFX file!")
