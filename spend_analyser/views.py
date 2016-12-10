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
    transactions = []
    
    if request.method == "POST":
        transactions = read_transactions(request.FILES['ofx_file'].file, session_id)
        save_transactions(transactions, session_id)
    transactions = Transaction.objects.filter(user=session_id).order_by('-date')
    
    chart_data = get_chart(Category.objects.all(), Transaction.objects.all())
    chart_labels = list(list(zip(*chart_data))[0])
    chart_values = list(list(zip(*chart_data))[1])
    
    subscriptions = Transaction.objects\
        .filter(subscription__isnull=False, user=session_id)\
        .values('name', 'subscription__name', 'subscription__company__name', \
                'subscription__company__category__name', 'subscription__description', 'subscription__monthly_price')\
        .distinct()
    print("Subscriptions: " + str(subscriptions))    
    print("Total transaction count: " + str(len(transactions)))
    return render(request, 'spend_analyser/transaction_list.html', {'transactions': transactions, 'chart_values': chart_values, 'chart_labels': chart_labels, 'subscriptions': subscriptions})

    # If transactions exist, perform analysis and show chart
    if Transaction.objects.all().count() > 0:
        chart_data = get_chart(Category.objects.all(), Transaction.objects.all())
        chart_labels = list(list(zip(*chart_data))[0])
        chart_values = list(list(zip(*chart_data))[1])
    # print("Result: " + str(len(transactions)))
        return render(request, 'spend_analyser/transaction_list.html', {'transactions': transactions, 'chart_values': chart_values, 'chart_labels': chart_labels, })

    # If no transactions exist, don't show anything
    else:
        return render(request, 'spend_analyser/transaction_list.html', {'transactions': transactions,})

def get_chart(categories, transactions):
    category_totals = {}  # Initialise dictionary which will store totals for each category
    overall_total = 0

    for transaction in transactions:
        category_totals[transaction.category.name] = category_totals.get(transaction.category.name, 0) - transaction.amount  # minus to invert sign
        overall_total -= transaction.amount

    for key in category_totals:
        print("%s: %d" % (key, category_totals[key]))

    # Remove Other category to find top 4 non-Other categories
    other_total = category_totals.pop(DEFAULT_TRANSACTION_CATEGORY)

    print(other_total)

    sorted_categories = sorted(category_totals, key=category_totals.get, reverse=True)[:4] # get top 4 non-Other categories in sorted list

    # Calculate total spend in top 4 non-Other categories
    top_total = 0
    for top_cat in sorted_categories:
        top_total += category_totals[top_cat]

    # Add back Other category and recalculate to include all categories not within top 4
    sorted_categories.append(DEFAULT_TRANSACTION_CATEGORY)
    category_totals[DEFAULT_TRANSACTION_CATEGORY] = overall_total - top_total

    chart_data = [(cat, round(category_totals.get(cat, 0), 2)) for cat in sorted_categories]

    return chart_data
