"""
    Views that will have a button automatically added for them in the
    admin section of the /analyse page.
    To add a new button, all you have to do is add a new entry in urls_admin.py
"""
from django.db.models import Q
from django.shortcuts import redirect, render

from monosaur.models import FixtureCompany, Category, Company
from spend_analyser.transactions import transaction_handler
from monosaur.utils import string_utils

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


PREFIX_NAME = "name-"
PREFIX_CATEGORY = "category-"


def categorise(request):
    content = {}
    
    if request.method == "POST":
        save_completed_companies(request.POST)
    
    content['companies'] = FixtureCompany.objects.all()
    content['categories'] = Category.objects.all()
    content['name_prefix'] = PREFIX_NAME
    content['category_prefix'] = PREFIX_CATEGORY
    
    return render(request, 'monosaur/categorise.html', content)

def save_completed_companies(form_data):
    for key in form_data.keys():
        if key.startswith(PREFIX_CATEGORY):
            if form_data[key] != "-1":
                category = form_data[key]
            else:
                category = None
            FixtureCompany.objects.filter(pk=key[len(PREFIX_CATEGORY):]).update(category_id = category)
        elif key.startswith(PREFIX_NAME):
            name = form_data[key]
            if not name:
                name = None

            FixtureCompany.objects.filter(pk=key[len(PREFIX_NAME):]).update(name = name)
            
    for fixture_company in FixtureCompany.objects.exclude(Q(name=u'') | Q(name=None) | Q(category=None)):
        Company(name = fixture_company.name, reference = fixture_company.reference, category = fixture_company.category).save()
        fixture_company.delete()
        
    FixtureCompany.save_to_fixture()
    Company.save_to_fixture()
