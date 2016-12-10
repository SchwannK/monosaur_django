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
    
    class Meta:
        unique_together = (('name', 'amount', 'date'),)
    
    def __str__(self):
        return "\n".join([self.name, str(self.amount) + "GBP", str(self.date), str(self.category), str(self.subscription)])
