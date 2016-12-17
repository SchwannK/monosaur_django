from django.shortcuts import render, redirect

from spend_analyser.transactions import transaction_handler
from subscriptions.models import Subscription
from monosaur.models import Category
from subscriptions.utils import subscription_filter_utils


def subscriptions(request):
    subscriptions = Subscription.objects.order_by('company__name')
    categories = subscription_filter_utils.get_subscription_categories(Subscription.objects.all())
    return render(request, 'subscriptions/subscriptions.html', {'navbar':'subscriptions', 'subscriptions': subscriptions, 'categories': categories,})
