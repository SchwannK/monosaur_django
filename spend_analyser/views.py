from django.shortcuts import render

from monosaur.models import Category
from monosaur.cookie import get_session_id

from .models import Transaction
from .transactions.constants import DEFAULT_TRANSACTION_CATEGORY
from .transactions.ofx_helper import read_transactions
from .transactions.transactions import save_transactions


# Create your views here.
def spend_analyser(request):
    print("==================== spend_analyser ======================")
    session_id = get_session_id(request, False)
    
    if request.method == "POST":
        transactions = read_transactions(request.FILES['ofx_file'].file)
        save_transactions(transactions, session_id)
    transactions = Transaction.objects.filter(user=session_id).order_by('-date')
    
    chart_data = get_chart(Category.objects.all(), Transaction.objects.all())
    chart_labels = list(list(zip(*chart_data))[0])
    chart_values = list(list(zip(*chart_data))[1])
    print("Result: " + str(len(transactions)))
    return render(request, 'spend_analyser/transaction_list.html', {'transactions': transactions, 'chart_values': chart_values, 'chart_labels': chart_labels, })


def get_chart(categories, transactions):
    category_totals = {}  # Initialise dictionary which will store totals for each category
    overall_total = 0

    for category in categories:
        category_totals[category.name] = 0  # Initialise all totals to 0

    for transaction in transactions:
        category_totals[transaction.category] = category_totals.get(transaction.category, 0) - transaction.amount  # minus to invert sign
        overall_total -= transaction.amount

#     other_total = category_totals.pop(DEFAULT_TRANSACTION_CAT)

    sorted_categories = sorted(category_totals, key=category_totals.get, reverse=True)[:4]
    top_total = 0
    for top_cat in sorted_categories:
        top_total += category_totals[top_cat]

    sorted_categories.append(DEFAULT_TRANSACTION_CATEGORY)
    
    if DEFAULT_TRANSACTION_CATEGORY in category_totals:
        category_totals[DEFAULT_TRANSACTION_CATEGORY] = overall_total - top_total

    chart_data = [(cat, round(category_totals.get(cat, 0), 2)) for cat in sorted_categories]

    # for key, value in chart_data:
    #    print("%s: %d" % (key, value))

    return chart_data
