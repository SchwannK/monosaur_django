"""
    Views that will have a button automatically added for them in the
    admin section of the /analyse page.
    To add a new button, all you have to do is add a new entry in urls_admin.py
"""
from django.contrib import auth
from django.forms import modelformset_factory
from django.shortcuts import redirect, render

from monosaur.models import Company
from subscriptions.models import Subscription
from spend_analyser.transactions import transaction_handler


def company(request):
    CompaniesFormSet = modelformset_factory(Company, fields=['reference', 'name', 'category'], extra = 3)

    if request.method == "POST":
        formset = CompaniesFormSet(request.POST or None)
        if formset.is_valid():
            formset.save()
            formset = CompaniesFormSet(queryset=Company.objects.order_by('-pk'))
    else:
        formset = CompaniesFormSet(queryset=Company.objects.order_by('-pk'))

    content = {'formset': formset}
    
    return render(request, 'monosaur/companies.html', content)

def subscription(request):
    SubscriptionsFormSet = modelformset_factory(Subscription, fields='__all__', extra=3)
    
    if request.method == "POST":
        formset = SubscriptionsFormSet(request.POST or None)
        if formset.is_valid():
            formset.save()
            formset = SubscriptionsFormSet(queryset=Subscription.objects.order_by('-pk'))
    else:
        formset = SubscriptionsFormSet(queryset=Subscription.objects.order_by('-pk'))
    content = {'formset': formset}
    
    return render(request, 'monosaur/subscriptions.html', content)
    

def db_cleanup(request):
    transaction_handler.delete_old_entries()
    return redirect("/analyse")

def db_clear(request):
    transaction_handler.delete_all_entries()
    return redirect("/analyse")

def delete(request, table, pk):
    if request.user.is_superuser:
        if table=='company':
            Company.objects.filter(pk=pk).delete()
            Company.save_to_fixture()
        elif table=='subscription':
            Subscription.objects.filter(pk=pk).delete()
            Subscription.save_to_fixture()
    return redirect(request.GET.get('next', '/analyse'))

def logout(request):
    auth.logout(request)
    return redirect(request.GET.get('next', '/analyse'))
