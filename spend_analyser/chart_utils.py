from spend_analyser.transactions.constants import DEFAULT_TRANSACTION_CATEGORY


def get_chart(categories, transactions):
    category_totals = {}  # Initialise dictionary which will store totals for each category
    overall_total = 0

    for transaction in transactions:
        category_totals[transaction.category.name] = category_totals.get(transaction.category.name, 0) - transaction.amount  # minus to invert sign
        overall_total -= transaction.amount

    # Remove Other category to find top 4 non-Other categories
    if DEFAULT_TRANSACTION_CATEGORY in category_totals:
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
