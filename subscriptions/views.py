from django.shortcuts import render

from monosaur.models import Subscription


def subscriptions(request):
    subscriptions = Subscription.objects.order_by('company__name')
    return render(request, 'subscriptions/subscriptions.html', {'subscriptions': subscriptions})
