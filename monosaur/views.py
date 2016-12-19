"""
    Views that will have a button automatically added for them in the
    admin section of the /analyse page.
    To add a new button, all you have to do is add a new entry in urls_admin.py
"""
from django.contrib import auth
from django.db import IntegrityError, transaction
from django.forms import modelformset_factory, modelform_factory, formset_factory
from django.forms.models import BaseModelFormSet
from django.shortcuts import redirect, render

from monosaur.models import Company, Uncategorised
from spend_analyser.transactions import transaction_handler
from subscriptions.models import Subscription

from .forms import UncategorisedForm


def company(request):
    fields = ['reference', 'name', 'category']
    response = get_response(request, 'monosaur/companies.html', Company, extra=3, fields=fields)
    return response

def subscription(request):
    fields = ['reference', 'company', 'name', 'description', 'monthly_price', 'subscription_url']
    response = get_response(request, 'monosaur/subscriptions.html', Subscription, extra=2, fields=fields)
    return response

def uncategorised(request):
    if not request.user.is_superuser:
        return redirect("/admin")
    FormSet = get_formset(request, Uncategorised, UncategorisedForm, extra=0)
    formset, valid = save_formset(request, Uncategorised, FormSet)
    content = {'formset': formset}
    
    if not valid:
        content['error_message'] = 'See errors below!'
    else:
        if "save_migrate" in request.POST:
            FormSet = modelformset_factory(Uncategorised, fields='__all__')
            formset = FormSet(request.POST or None)
            migrate_count = 0
            
            for form in formset:
                if form.is_valid():
                    uncategorised = form.instance
                    if uncategorised.all_set():
                        try:
                            with transaction.atomic():
                                Company(name=uncategorised.name, reference=uncategorised.reference, category=uncategorised.category).save()
                                uncategorised.delete()
                                migrate_count += 1
                        except IntegrityError as e:
                            content['error_message'] = str(e) 
                            pass
            if migrate_count > 0:
                content['success_message'] = 'Migrated %d companies' % migrate_count

    return render(request, 'monosaur/uncategorised.html', content)

def get_response(request, target_url, model, form=None, extra=3, fields='__all__'):
    if not request.user.is_superuser:
        return redirect("/admin")
    FormSet = get_formset(request, model, form, extra=extra, fields=fields)
    formset, valid = save_formset(request, model, FormSet)
    content = {'formset': formset}
    
    if not valid:
        content['error_message'] = 'See errors below!'

    return render(request, target_url, content)

def get_formset(request, model, form=None, extra=3, fields='__all__'):
    if form:
        FormSet = formset_factory(form, formset=BaseModelFormSet, extra=extra)
    else:
        # inferring the form from the model
        FormSet = modelformset_factory(model, fields=fields, extra=extra)
    FormSet.model = model
    return FormSet

def save_formset(request, model, FormSet):
    valid = True
    
    if request.method == "POST":
        formset = FormSet(request.POST or None)
        valid = formset.is_valid()
        if valid:
            formset.save()
            model.save_to_fixture()
            formset = FormSet(queryset=model.objects.order_by('-pk'))
    else:
        formset = FormSet(queryset=model.objects.order_by('-pk'))
    return formset, valid    

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
        if table == 'company':
            deleted, row_count = Company.objects.filter(pk=pk).delete()
            Company.save_to_fixture()
        elif table == 'subscription':
            deleted, row_count = Subscription.objects.filter(pk=pk).delete()
            Subscription.save_to_fixture()
        elif table == 'uncategorised':
            deleted, row_count = Uncategorised.objects.filter(pk=pk).delete()
            Uncategorised.save_to_fixture()
        else:
            print('Unknown table: ' + table)
    return redirect(request.GET.get('next', '/analyse'))

def migrate(request, from_table, what_pk, to_table):
    print('Migrating ' + from_table + "/" + what_pk + " to " + to_table)
    if not request.user.is_superuser:
        return redirect("/admin")
    if request.user.is_superuser:
        if from_table == to_table:
            print('Promote into the same table??')
        else:
            if from_table == 'company':
                if to_table == 'subscription':
                    company = Company.objects.get(pk=what_pk)
                    Subscription(company=company, reference=company.reference, name=company.name).save()
                elif to_table == 'uncategorised':
                    print('Not yet implemented')
                else:
                    print('Unknown table: ' + to_table)
            elif from_table == 'subscription':
                if to_table == 'company':
                    print('Not yet implemented')
                elif to_table == 'uncategorised':
                    print('Not yet implemented')
                else:
                    print('Unknown table: ' + to_table)
            elif from_table == 'uncategorised':
                if to_table == 'company':
                    uncategorised = Uncategorised.objects.get(pk=what_pk)
                    Company(name=uncategorised.name, reference=uncategorised.reference, category=uncategorised.category).save()
                    uncategorised.delete()
                elif to_table == 'subscription':
                    print('Not yet implemented')
                else:
                    print('Unknown table: ' + to_table)
            else:
                print('Unknown table: ' + from_table)
    else:
        print('No superuser')
    return redirect(request.GET.get('next', '/analyse'))

def logout(request):
    if not request.user.is_superuser:
        return redirect("/admin")
    auth.logout(request)
    return redirect(request.GET.get('next', '/analyse'))
