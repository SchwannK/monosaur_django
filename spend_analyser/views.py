from django.shortcuts import render, redirect

from monosaur import cookie
from monosaur.models import Category, FixtureCompany
from monosaur.utils import admin_utils
from spend_analyser.models import Transaction, Session
from spend_analyser.transactions import transaction_handler
from spend_analyser.utils import chart_utils


def spend_analyser(request):
    session = cookie.get_session(request, False)

    content = {'navbar':'spend_analyser', }

    if request.method == "POST":
        print(str(type(request.user)))
        if 'selected_session' in request.POST and request.user.is_superuser:
            if "session_select" in request.POST:
                session = Session.objects.get(session_id=request.POST['selected_session'])
            elif "session_delete" in request.POST:
                Session.objects.get(session_id=request.POST['selected_session']).delete()
                return redirect("/analyse")
        positive_message, negative_message = process_transactions(request.FILES.getlist('file'), session)
        content['positive_message'] = positive_message
        content['negative_message'] = negative_message

    transactions = Transaction.objects.filter(session__session_id=session.session_id).order_by('-date')
    content['transactions'] = transactions

    content['subscriptions'] = Transaction.objects\
        .filter(subscription__isnull=False, session__session_id=session.session_id)\
        .values('name', 'subscription__name', 'subscription__company__name', \
                'subscription__company__category__name', 'subscription__description', \
                'subscription__monthly_price', 'subscription__subscription_url')\
        .distinct()

    content['admin_methods'] = admin_utils.get_admin_methods()
    content['sessions'] = admin_utils.get_sessions()

    # If transactions exist, perform analysis and show chart
    if len(transactions) > 0:
        if len(chart_utils.create_date_array(transactions)) > 1:
            # Process data for line chart if more than one month of data
            content['chartjs_linedata'] = chart_utils.get_linechart_data(Category.objects.all(), transactions)

        else:
            # Else process data for bar chart
            content['chartjs_bardata'] = chart_utils.get_barchart_data(Category.objects.all(), transactions)

    return render(request, 'spend_analyser/transaction_list.html', content)

def process_transactions(files, session):
    positive_message = None
    negative_message = None
    successFiles = []
    errorFiles = []
    total_read_count = 0
    total_save_count = 0

    for file in files:
        read_count, save_count = transaction_handler.process_file(file, session, successFiles, errorFiles)
        total_read_count += read_count
        total_save_count += save_count

    separator = '<p class="tab">'
    if total_read_count > 0:
        positive_message = '%d transactions (%d new) captured from:%s%s' % (total_read_count, total_save_count, separator, '<br>'.join(successFiles))

    if len(errorFiles) > 0:
        negative_message = 'No transactions captured from:%s%s' % (separator, '<br>'.join(errorFiles))

    print ("Success report: " + str(positive_message))
    print ("Error report: " + str(negative_message))

    return positive_message, negative_message
