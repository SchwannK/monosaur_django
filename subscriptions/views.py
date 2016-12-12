from django.shortcuts import render, redirect

from spend_analyser.transactions import transaction_handler
from subscriptions.models import Subscription


def subscriptions(request):
    subscriptions = Subscription.objects.order_by('company__name')
    return render(request, 'subscriptions/subscriptions.html', {'navbar':'subscriptions', 'subscriptions': subscriptions})
