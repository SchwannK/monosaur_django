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
    if not request.user.is_superuser:
        return redirect("/admin")
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
    if not request.user.is_superuser:
        return redirect("/admin?next=www.google.com")
    SubscriptionsFormSet = modelformset_factory(Subscription, fields=['reference', 'company', 'name', 'description', 'monthly_price', 'subscription_url'], extra=2)
    
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
    if not request.user.is_superuser:
        return redirect("/admin")
    transaction_handler.delete_old_entries()
    return redirect("/analyse")

def db_clear(request):
    if not request.user.is_superuser:
        return redirect("/admin")
    transaction_handler.delete_all_entries()
    return redirect("/analyse")

def delete(request, table, pk):
    if not request.user.is_superuser:
        return redirect("/admin")
    if request.user.is_superuser:
        if table=='company':
            deleted, row_count = Company.objects.filter(pk=pk).delete()
            Company.save_to_fixture()
        elif table=='subscription':
            deleted, row_count = Subscription.objects.filter(pk=pk).delete()
            Subscription.save_to_fixture()
    return redirect(request.GET.get('next', '/analyse'))

def logout(request):
    if not request.user.is_superuser:
        return redirect("/admin")
    auth.logout(request)
    return redirect(request.GET.get('next', '/analyse'))

def promote_to_subscription(request, pk):
    if not request.user.is_superuser:
        return redirect("/admin")
    company = Company.objects.get(pk=pk)
    subscription = Subscription(company=company, reference=company.reference, name=company.name)
    subscription.save()
    print(str(subscription.pk))
    return redirect(request.GET.get('next', '/analyse'))