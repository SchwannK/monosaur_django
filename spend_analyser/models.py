from django.db import models

from monosaur.models import Category
from subscriptions.models import Subscription


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
