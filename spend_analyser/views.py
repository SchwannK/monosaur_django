from django.db import connection
from django.shortcuts import render, redirect
import pdfcrowd

from monosaur import cookie
from monosaur.models import Category
from monosaur.utils import admin_utils, cursor_utils
from spend_analyser.models import Transaction, Session
from spend_analyser.transactions import transaction_handler
from spend_analyser.utils import chart_utils

from .transactions import constants


def spend_analyser(request, session_id=None):
    if session_id:
        session = cookie.get_session(session_id)
    else:
        session = cookie.extract_session(request, False)

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
        .values('subscription__name', 'subscription__company__name', \
                'subscription__company__category__name', 'subscription__description', \
                'subscription__monthly_price')\
        .order_by('subscription__name')\
        .distinct()

    # update all transactions the category id of which is incorrect
    cursor = connection.cursor()
    query = "SELECT reference as ref, id FROM spend_analyser_transaction WHERE session_id = '%s' AND COALESCE(category_id, -1) <> (SELECT COALESCE((SELECT category_id FROM monosaur_company WHERE ref LIKE '%%' || monosaur_company.reference || '%%' LIMIT 1), (SELECT id FROM monosaur_category WHERE name='%s')))" % (session.pk, constants.DEFAULT_TRANSACTION_CATEGORY)
    cursor.execute(query)
    for row in cursor_utils.dictfetchall(cursor):
        transaction = Transaction.objects.get(pk=row['id'])
        transaction.category = transaction_handler.get_category(transaction.reference)
        
        if transaction.category:
            print('Updating transaction ' + transaction.reference + ' to category ' + transaction.category.name)
        else:
            print('Updating transaction ' + transaction.reference + ' to category None')
        transaction.save()

    # update all transactions the subscription id of which is incorrect
    cursor = connection.cursor()
    query = "SELECT reference as ref, id FROM spend_analyser_transaction WHERE session_id = '%s' AND COALESCE(subscription_id, -1) <> (SELECT COALESCE((SELECT id FROM subscriptions_subscription WHERE ref LIKE '%%' || subscriptions_subscription.reference || '%%' LIMIT 1), -1))" % session.pk
    cursor.execute(query)
    for row in cursor_utils.dictfetchall(cursor):
        transaction = Transaction.objects.get(pk=row['id'])
        transaction.subscription = transaction_handler.get_subscription(transaction.reference)
        
        if transaction.subscription:
            print('Updating transaction ' + transaction.reference + ' to subscription ' + transaction.subscription.name)
        else:
            print('Updating transaction ' + transaction.reference + ' to subscription None')
        transaction.save()

#     # This is just for debugging.
#     flag = True
#     for t in Transaction.objects.filter(session = session):
#         sub = transaction_handler.get_subscription(t.reference)
#         if sub:
#             if t.subscription_id != sub.pk:
#                 if flag:
#                     print('Failed to update these subscriptions: ')
#                     flag = False
#                 print(str(t.subscription_id) + "\t" + str(t.pk) + ":\t"+ str(sub.pk) + "\t\t" + t.reference)
#         else:
#             if t.subscription_id:
#                 if flag:
#                     print('Failed to update these subscriptions: ')
#                     flag = False
#                 print(str(t.subscription_id) + "\t" + str(t.pk) + ":\tNone\t\t" + t.reference)
# 
#     flag = True
#     for t in Transaction.objects.filter(session = session):
#         cat = transaction_handler.get_category(t.reference)
#         if cat:
#             if t.category_id != cat.pk:
#                 if flag:
#                     print('Failed to update these categories: ')
#                     flag = False 
#                 print(str(t.category_id) + "\t" + str(t.pk) + ":\t"+ str(cat.pk) + "\t\t" + t.reference)
#         else:
#             if t.category_id:
#                 if flag:
#                     print('Failed to update these categories: ')
#                     flag = False 
#                 print(str(t.category_id) + "\t" + str(t.pk) + ":\tNone\t\t" + t.reference)

    content['admin_methods'] = admin_utils.get_admin_methods()
    content['sessions'] = admin_utils.get_sessions()

    # If transactions exist, perform analysis and show chart
    if len(transactions) > 0:
        if len(chart_utils.create_date_array(transactions)) > 1:
            # Process data for line chart and overall bar chart if more than one month of data
            content['chartjs_linedata'] = chart_utils.get_linechart_data(Category.objects.all(), transactions)
            content['chartjs_bardata'] = chart_utils.get_barchart_data(Category.objects.all(), transactions)

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

def print_to_pdf(request):
    pageclan = spend_analyser(request)
    html = str(pageclan.content)
    client = pdfcrowd.Client("arlecchino", "fb890ee085fc87bd3e4e989a0b5805b0")
    client.setPageLayout(pdfcrowd.FIT_HEIGHT)
    client.setInitialPdfZoomType(1)
    client.setPdfScalingFactor(0.003)
    print(html)
    output_file = open('C:/html.pdf', 'wb')
    pdf = client.convertHtml(html, output_file)
    output_file.close()
    return pageclan