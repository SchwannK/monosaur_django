from django.db import models
from ofxparse import OfxParser

from monosaur.models import Category, Subscription


class Transaction(models.Model):
    name = models.CharField(max_length=100)
    amount = models.FloatField()
    date = models.DateField()
    category = models.ForeignKey(Category)
    subscription = models.ForeignKey(
        Subscription, null=True, blank=True
    )
    user = models.CharField(max_length=40, null=True)
    
    def __str__(self):
        return self.name
