from django.shortcuts import render

from monosaur.cookie import get_session_id
from subscriptions.models import Subscription


def subscriptions(request):
    print("==================== subscriptions ======================")
    subscriptions = Subscription.objects.order_by('company__name')
    return render(request, 'subscriptions/subscriptions.html', {'navbar':'subscriptions', 'subscriptions': subscriptions})
