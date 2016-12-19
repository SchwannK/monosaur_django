from django import forms
from django.forms.widgets import TextInput

from .models import Uncategorised


class UncategorisedForm(forms.ModelForm):
    class Meta:
        model = Uncategorised
        fields=['reference', 'name', 'category']
        widgets = {
            'reference': TextInput(attrs={'style': 'width: 100%'}),
            'name': TextInput(attrs={'style': 'width: 100%'}),
        }
