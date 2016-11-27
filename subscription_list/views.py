from django.shortcuts import render

# Create your views here.

def subscription_list(request):
    return render(request, 'subscription_list/subscription_list.html', {})
