from django.core.urlresolvers import get_resolver
from django.shortcuts import redirect

from spend_analyser.transactions import transaction_handler


def database_cleanup(request):
    transaction_handler.delete_old_entries()
    return redirect("/analyse")

def database_clear(request):
    transaction_handler.delete_all_entries()
    return redirect("/analyse")

def database_test(request):
    
    return redirect("/analyse")
