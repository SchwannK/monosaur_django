from django.shortcuts import render

from monosaur import cookie
from monosaur.models import Category, FixtureCompany
from monosaur.utils import admin_utils
from spend_analyser.models import Transaction
from spend_analyser.transactions import transaction_handler
from spend_analyser.transactions.ofx_helper import OfxHelper
from spend_analyser.transactions.qif_helper import QifHelper
from spend_analyser.utils import chart_utils


def spend_analyser(request):
    session = cookie.get_session(request, False)

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

    content['admin_methods'] = admin_utils.get_admin_methods()

    # If transactions exist, perform analysis and show chart
    if len(transactions) > 0:
        if len(chart_utils.create_date_array(transactions)) > 1:
            # Process data for line chart if more than one month of data
            content['chartjs_linedata'] = chart_utils.get_linechart_data(Category.objects.all(), transactions)

        else:
            # Else process data for bar chart
            content['chartjs_bardata'] = chart_utils.get_barchart_data(Category.objects.all(), transactions)

    return render(request, 'spend_analyser/transaction_list.html', content)

def handle_files(files, session, result_dict):
    good_files_message = ''
    bad_files_message = ''
    successFiles = []
    errorFiles = []
    total_read_count = 0
    total_save_count = 0

    for file in files:
        read_count = 0
        parsers = [OfxHelper(), QifHelper()] # add new parsers here
        transactions = []

        for parser in parsers:
            try:
                transactions = parser.read_transactions(file, session)

                if transactions and len(transactions) > 0:
                    read_count = len(transactions)
                
                # in the above read_transactions method, all new companies were inserted to FixtureCompany
                # let's export it so we don't lose them on the next db reset
                FixtureCompany.save_to_fixture()
            except Exception as e:
                print("==== error parsing with " + str(parser) + ": " + str(e))
#                 traceback.print_exc()
#                 raise e
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
