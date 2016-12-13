
import traceback

from django.shortcuts import render

from monosaur.cookie import get_session
from monosaur.models import Category, FixtureCompany
from spend_analyser.transactions import transaction_handler

from .utils.chart_utils import *
from .models import Transaction
from .transactions.ofx_helper import OfxHelper
from .transactions.qif_helper import QifHelper
from .utils.admin_utils import get_admin_methods


def spend_analyser(request):
    session = get_session(request, False)

    content = {'navbar':'spend_analyser', }

    if request.method == "POST":
        handle_files(request.FILES.getlist('file'), session, content)

    transactions = Transaction.objects.filter(session__session_id=session.session_id).order_by('-date')
    content['transactions'] = transactions

    content['subscriptions'] = Transaction.objects\
        .filter(subscription__isnull=False, session__session_id=session.session_id)\
        .values('name', 'subscription__name', 'subscription__company__name', \
                'subscription__company__category__name', 'subscription__description', 'subscription__monthly_price')\
        .distinct()
        
    content['admin_methods'] = get_admin_methods()
    # If transactions exist, perform analysis and show chart
    if len(transactions) > 0:
        content['chartjs_data'] = get_chart(Category.objects.all(), transactions)
        content['chartjs_linedata'] = get_chart_new(Category.objects.all(), transactions)
        
    return render(request, 'spend_analyser/transaction_list.html', content)

def handle_files(files, session, result_dict):
    good_files_message = ''
    bad_files_message = ''
    successFiles = []
    errorFiles = []
    total_read_count = 0;
    total_save_count = 0;

    for file in files:
        read_count = 0
        parsers = [OfxHelper(), QifHelper()] # add new parsers here
        transactions = []

        for parser in parsers:
            try:
                transactions = parser.read_transactions(file, session)

                if transactions and len(transactions) > 0:
                    read_count = len(transactions)
                        
                FixtureCompany.dump()
            except Exception as e:
                print("==== error parsing with " + str(parser))
                traceback.print_exc()
                raise e
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
    
    result_dict['good_files_message'] = good_files_message
    result_dict['bad_files_message'] = bad_files_message