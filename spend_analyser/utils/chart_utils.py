"""
    This class provides the formatted data for the pretty charts at /analyse
"""
import collections

from dateutil.relativedelta import relativedelta
from django.db.models import Max, Min

from spend_analyser.transactions.constants import *

"""
This method provides bar chart data for the 5 largest non-'Other' transaction categories (for recognised transactions)
"""
def get_barchart_data(categories, transactions):
    category_totals = {}  # Initialise dictionary which will store totals for each category
    overall_total = 0

    for transaction in transactions:
        if transaction.category.name is not DEFAULT_TRANSACTION_CATEGORY:
            category_totals[transaction.category.name] = category_totals.get(transaction.category.name, 0) - transaction.amount  # minus to invert sign
            overall_total -= transaction.amount

    # Remove Other category to find top 5 non-Other categories
    if DEFAULT_TRANSACTION_CATEGORY in category_totals:
        other_total = category_totals.pop(DEFAULT_TRANSACTION_CATEGORY)

    sorted_categories = sorted(category_totals, key=category_totals.get, reverse=True)[:5]  # get top 5 non-Other categories in sorted list

    chart_data = [(cat, round(category_totals.get(cat, 0), 2)) for cat in sorted_categories]

    chart_labels = list(list(zip(*chart_data))[0])
    chart_values = list(list(zip(*chart_data))[1])

    chartjs_data = {}
    chartjs_data["chart_labels"] = chart_labels
    chartjs_data["chart_values"] = chart_values
    chartjs_data["colours"] = CHART_JS_COLORS
    chartjs_data["month"] = create_date_array(transactions)[0]

    return chartjs_data


def get_largest_categories(categories, transactions):
    category_totals = {}  # Initialise dictionary which will store totals for each category
    overall_total = 0

    for transaction in transactions:
        category_totals[transaction.category.name] = category_totals.get(transaction.category.name, 0) - transaction.amount  # minus to invert sign
        overall_total -= transaction.amount

    # Remove Other category to find top 4 non-Other categories
    if DEFAULT_TRANSACTION_CATEGORY in category_totals:
        other_total = category_totals.pop(DEFAULT_TRANSACTION_CATEGORY)
        print(other_total)

    largest_categories = sorted(category_totals, key=category_totals.get, reverse=True)[:5]  # get top 5 non-Other categories in sorted list

    return largest_categories

# Returns array of Month-Year values from transaction values
def create_date_array(transactions):

    date_max = transactions.aggregate(Max('date'))['date__max']
    date_min = transactions.aggregate(Min('date'))['date__min']

    date_array = []

    # If all data is in the same month, then add just that month to array
    if date_max.strftime('%b %y') == date_min.strftime('%b %y'):
        date_array.append(date_max.strftime('%b %y'))

    # Else add months from date_min to date_max inclusive into array
    else:
        current = date_min
        while not current.strftime('%b %y') in date_max.strftime('%b %y'):
            date_array.append(current.strftime('%b %y'))
            current += relativedelta(months=1)
        date_array.append(current.strftime('%b %y'))

    return date_array

"""
This method provides line chart data for the 5 largest non-'Other' transaction categories (for recognised transactions)
"""
def get_linechart_data(categories, transactions):
    total_spend = collections.OrderedDict()  # Initialise top level dictionary storing totals by month by category

    largest_categories = get_largest_categories(categories, transactions)

    date_array = create_date_array(transactions)

    for category in largest_categories:
        total_spend[category] = collections.OrderedDict()  # Initialise dictionaries for categories
        for date in date_array:
            total_spend[category][date] = 0  # Initialise all possible values of category-date to 0

    for transaction in transactions:
        if transaction.amount < 0:
            if transaction.category.name in largest_categories:
                total_spend[transaction.category.name][transaction.date.strftime('%b %y')] = total_spend.get(transaction.category.name).get(transaction.date.strftime('%b %y')) - transaction.amount

    chartjs_data = {}
    chartjs_data['months'] = date_array  # Months for Chartjs
    chartjs_data['data'] = {}
    colour_index = 0  # initialise index for chart colours
    for category in largest_categories:
        # Assign list of total spend values (rounded to 2 d.p.) to each category and chart colour by tuple (spend_values, chart_colours)
        chartjs_data['data'][category] = (list(round(value, 2) for value in total_spend[category].values()), CHART_JS_COLORS[colour_index])

        colour_index += 1

    return chartjs_data
