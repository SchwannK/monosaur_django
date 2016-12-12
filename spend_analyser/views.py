
import traceback

from django.shortcuts import render, redirect

from monosaur.cookie import get_session
from monosaur.models import Category
from spend_analyser.transactions import transaction_handler

from .chart_utils import *
from .models import Transaction
from .transactions.ofx_helper import OfxHelper
from .transactions.qif_helper import QifHelper


def spend_analyser(request):
    session = get_session(request, False)
    transactions = []

    if request.method == "POST":
        try:
            transactions = QifHelper().read_transactions(request.FILES['file'].file, session)
        except Exception as e:
            print("error parsing qif file")
            traceback.print_exc()
            try:
                transactions = OfxHelper().read_transactions(request.FILES['file'].file, session)
            except Exception as e:
                print("error parsing ofx file")
                raise e
        transaction_handler.save(transactions)
    transactions = Transaction.objects.filter(session__session_id=session.session_id).order_by('-date')

    subscriptions = Transaction.objects\
        .filter(subscription__isnull=False, session__session_id=session.session_id)\
        .values('name', 'subscription__name', 'subscription__company__name', \
                'subscription__company__category__name', 'subscription__description', 'subscription__monthly_price')\
        .distinct()

    # If transactions exist, perform analysis and show chart
    if len(transactions) > 0:
        chartjs_data = get_chart(Category.objects.all(), Transaction.objects.all())
        chartjs_linedata = get_chart_new(Category.objects.all(), Transaction.objects.all())

        return render(request, 'spend_analyser/transaction_list.html', {'navbar':'spend_analyser', 'transactions': transactions, 'chartjs_data': chartjs_data, 'chartjs_linedata': chartjs_linedata, 'subscriptions': subscriptions})

    # If no transactions exist, don't show anything
    else:
        return render(request, 'spend_analyser/transaction_list.html', {'navbar':'spend_analyser', 'transactions': transactions})

def database_cleanup(request):
    transaction_handler.delete_old_entries()
    return redirect("/analyse")
