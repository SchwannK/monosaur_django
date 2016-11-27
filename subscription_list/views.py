from django.shortcuts import render
from .models import Subscription

# Create your views here.

def subscription_list(request):
    subscriptions = Subscription.objects.order_by('company_name')
    return render(request, 'subscription_list/subscription_list.html', {'subscriptions': subscriptions})
