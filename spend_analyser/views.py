
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
    good_files_message = ''
    bad_files_message = ''

    if request.method == "POST":
        successFiles = []
        errorFiles = []
        total_read_count = 0;
        total_save_count = 0;

        for file in request.FILES.getlist('file'):
            read_count = 0
            parsers = [QifHelper(), OfxHelper()] # add new parsers here
            transactions = []

            for parser in parsers:
                try:
                    transactions = parser.read_transactions(file, session)

                    if transactions and len(transactions) > 0:
                        read_count = len(transactions)
                except Exception as e:
                    print("==== error parsing with " + str(parser))
#                     traceback.print_exc()
                if read_count > 0:
                    break

            if read_count > 0:
                total_save_count += transaction_handler.save(transactions)
                successFiles.append(str(file))
                total_read_count += read_count
            else:
                errorFiles.append(str(file))

        separator = '<p class="tab">'
        if total_read_count > 0:
            good_files_message = '%d transactions captured from:%s%s%s(%d new)' % (total_read_count, separator, separator.join(successFiles), '<br>', total_save_count)

        if len(errorFiles) > 0:
            bad_files_message = 'No transactions captured from:%s%s' % (separator, separator.join(errorFiles))

        print ("Success: " + good_files_message)
        print ("Error: " + bad_files_message)

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

        return render(request, 'spend_analyser/transaction_list.html', {'navbar':'spend_analyser', 'transactions': transactions, 'chartjs_data': chartjs_data, 'chartjs_linedata': chartjs_linedata, 'subscriptions': subscriptions, 'good_files_message' : good_files_message, 'bad_files_message' : bad_files_message,})

    # If no transactions exist, don't show anything
    else:
        return render(request, 'spend_analyser/transaction_list.html', {'navbar':'spend_analyser', 'transactions': transactions, 'good_files_message' : good_files_message, 'bad_files_message' : bad_files_message, })

def database_cleanup(request):
    transaction_handler.delete_old_entries()
    return redirect("/analyse")
