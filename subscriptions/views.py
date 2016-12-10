from django.shortcuts import render

from monosaur.cookie import get_session_id
from subscriptions.models import Subscription


def subscriptions(request):
    print("==================== subscriptions ======================")
<<<<<<< HEAD
    session_id = get_session_id(request, False)
    transactions = Transaction.objects\
        .filter(subscription__isnull=False, user=session_id)\
        .values('name', 'subscription__name', 'subscription__company__name', \
                'subscription__company__category__name', 'subscription__description', 'subscription__monthly_price')\
        .distinct()
    print("Result: " + str(transactions))
    return render(request, 'subscriptions/subscriptions.html', {'navbar':'subscriptions', 'subscriptions': transactions})
=======
    subscriptions = Subscription.objects.order_by('company__name')
    return render(request, 'subscriptions/subscriptions.html', {'subscriptions': subscriptions})

>>>>>>> origin/master
