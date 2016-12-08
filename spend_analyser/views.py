import io, operator

from django.shortcuts import render

from monosaur.utils import randomword

from .ofx_handler import *


# Create your views here.
def spend_analyser(request):
    session_id = None
    
    if 'sessionid' in request.COOKIES:
        session_id = request.COOKIES['sessionid']
 
    if session_id == None and 'mysessionid' in request.COOKIES:
        session_id = request.COOKIES['mysessionid']
     
    if session_id == None:
        session_id = "rand-" + randomword(30)
     
    print(session_id)
    
    if request.method == "POST":
        transactions = read_transactions(request.FILES['ofx_file'].file)
        save_transactions(transactions, session_id)
    transactions = Transaction.objects.order_by('-date')
    
    chart_data = get_chart()
    chart_labels = list(list(zip(*chart_data))[0])
    chart_values = list(list(zip(*chart_data))[1])
    
    response = render(request, 'spend_analyser/transaction_list.html', {'transactions': transactions, 'chart_values': chart_values, 'chart_labels': chart_labels, })
    
    response.cookies['mysessionid'] = session_id
    return response

