"""
    Views that will have a button automatically added for them in the
    admin section of the /analyse page.
    To add a new button, all you have to do is add a new entry in urls_admin.py
"""
from django.contrib import auth
from django.db import transaction
from django.forms import modelformset_factory
from django.shortcuts import redirect, render

from monosaur.models import FixtureCompany, Company
from spend_analyser.transactions import transaction_handler
from django.http.response import HttpResponseRedirect


def companies(request):
    FixtureCompaniesFormSet = modelformset_factory(FixtureCompany, fields=['reference', 'name', 'category'], extra=3)
    save_count = 0
    
    if request.method == "POST":
        formset = FixtureCompaniesFormSet(request.POST or None)
        if formset.is_valid():
            formset.save()
            if "save_migrate" in request.POST:
                save_count = migrate_complete_companies()
            formset = FixtureCompaniesFormSet(queryset=FixtureCompany.objects.order_by('-pk'))
    else:
        formset = FixtureCompaniesFormSet(queryset=FixtureCompany.objects.order_by('-pk'))

    content = {'formset': formset}
    
    if save_count > 0:
        content['success_message'] = str(save_count) + " companies saved and moved to <a href='http://localhost:8000/admin/monosaur/company/'>monosaur.Company</a>"
    
    return render(request, 'monosaur/companies.html', content)

def db_cleanup(request):
    transaction_handler.delete_old_entries()
    return redirect("/analyse")

def db_clear(request):
    transaction_handler.delete_all_entries()
    return redirect("/analyse")

def save_companies(request):
    FixtureCompany.save_to_fixture()
    return redirect("/analyse")

def load_companies(request):
    FixtureCompany.load_from_fixture()
    return redirect("/analyse")

def delete_fixture(request, pk):
    FixtureCompany.objects.filter(pk=pk).delete()
    FixtureCompany.save_to_fixture()
    return redirect("/admin/companies")

def logout(request):
    auth.logout(request)
    return redirect(request.GET.get('next', '/analyse'))

## Non API methods #######################################################################

# take all fixture companies that are fully specified and move them in the Company table
def migrate_complete_companies():
    save_count = 0
    complete_companies = FixtureCompany.objects.exclude(name__isnull=True).exclude(category_id__isnull=True)

    for c in complete_companies:
        try:
            with transaction.atomic():
                Company(name = c.name, reference = c.reference, category = c.category).save()
                c.delete()
                save_count += 1
        except:
            pass
    return save_count
