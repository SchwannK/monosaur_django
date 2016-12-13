from django.core.urlresolvers import get_resolver
from django.shortcuts import redirect

from spend_analyser.transactions import transaction_handler


def db_cleanup(request):
    transaction_handler.delete_old_entries()
    return redirect("/analyse")

def db_clear(request):
    transaction_handler.delete_all_entries()
    return redirect("/analyse")

def test(request):
    
    return redirect("/analyse")
