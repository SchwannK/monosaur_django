from django.shortcuts import render
from .models import Transaction

# Create your views here.

def spend_analyser(request):
    transactions = Transaction.objects.order_by('date')
    return render(request, 'spend_analyser/transaction_list.html', {'transactions': transactions})
