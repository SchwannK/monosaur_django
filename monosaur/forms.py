from django import forms
from django.forms.widgets import TextInput, Textarea

from .models import Uncategorised
from subscriptions.models import Subscription


class UncategorisedForm(forms.ModelForm):
    class Meta:
        model = Uncategorised
        fields=['reference', 'name', 'category']
        widgets = {
            'reference': TextInput(attrs={'style': 'width: 100%'}),
            'name': TextInput(attrs={'style': 'width: 100%'}),
        }

class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = Subscription
        fields=['reference', 'company', 'name', 'monthly_price', 'subscription_url', 'description']
        widgets = {
            'reference': Textarea(attrs={'placeholder': 'Reference...'}),
            'name': TextInput(attrs={'placeholder': 'Name...'}),
            'monthly_price': TextInput(attrs={'placeholder': 'Price...'}),
            'subscription_url': TextInput(attrs={'placeholder': 'Url...'}),
            'description': Textarea(attrs={'placeholder': 'Description...'}),
        }
