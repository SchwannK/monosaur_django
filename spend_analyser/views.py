from django.shortcuts import render

# Create your views here.

def spend_analyser(request):
    return render(request, 'spend_analyser/analytics.html', {})
