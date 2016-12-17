from monosaur.models import Category
from subscriptions.models import Subscription

def get_subscription_categories(subscriptions):

    all_subscription_categories = subscriptions.values_list('company__category__name', flat=True)

    return sorted(list(set(list(all_subscription_categories))))
