from django.shortcuts import render

from monosaur.cookie import get_session_id
from spend_analyser.models import Transaction
from django.contrib.sessions.middleware import SessionMiddleware


def subscriptions(request):
    SessionMiddleware
    print("==================== subscriptions ======================")
    session_id = get_session_id(request, False)
    transactions = Transaction.objects\
        .filter(subscription__isnull=False, user=session_id)\
        .values('name', 'subscription__name', 'subscription__company__name', \
                'subscription__company__category__name', 'subscription__description', 'subscription__monthly_price')\
        .distinct()
    print("Result: " + str(transactions))
    return render(request, 'subscriptions/subscriptions.html', {'navbar':'subscriptions', 'subscriptions': transactions})
