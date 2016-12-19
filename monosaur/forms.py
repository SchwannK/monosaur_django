from django import forms
from django.forms.widgets import TextInput, Textarea, Select

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
            'reference': Textarea(attrs={'placeholder': 'Reference...', 'style': 'width:100%;'}),
            'company': Select(attrs={'style': 'width:100%;'}),
            'name': TextInput(attrs={'placeholder': 'Name...', 'style': 'width:100%;'}),
            'monthly_price': TextInput(attrs={'placeholder': 'Price...', 'style': 'width:100%;'}),
            'subscription_url': TextInput(attrs={'placeholder': 'Url...', 'style': 'width:100%;'}),
            'description': Textarea(attrs={'placeholder': 'Description...', 'style': 'width:100%;'}),
        }
