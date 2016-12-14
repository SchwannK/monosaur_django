"""
    Views that will have a button automatically added for them in the
    admin section of the /analyse page.
    To add a new button, all you have to do is add a new entry in urls_admin.py
"""
from django.forms import modelformset_factory
from django.shortcuts import redirect, render

from monosaur.models import FixtureCompany, Company
from monosaur.utils import string_utils
from spend_analyser.transactions import transaction_handler


def companies(request):
    FixtureCompaniesFormSet = modelformset_factory(FixtureCompany, fields='__all__', extra=3)
    save_count = 0
    no_error = True
    
    if request.method == "POST":
        formset = FixtureCompaniesFormSet(request.POST or None)
        
#         if formset.is_valid():
        for form in formset:
            if form.is_valid():
                if form.instance.pk is not None:
                    instance = form.instance
                else:
                    instance = form.save(commit=False)
                instance.name = string_utils.to_none(instance.name)
                instance.reference = string_utils.to_none(instance.reference)
                try:
                    instance.save()
                except Exception as e:
                    pass

                if not string_utils.is_empty(instance.name) and not string_utils.is_empty(instance.reference) and instance.category:
                    try:
                        Company(name=instance.name, reference=instance.reference, category=instance.category).save()
                        save_count += 1
                    except Exception as e:
                        no_error = False
                    instance.delete()
            else:
                no_error = False

    if no_error:
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
