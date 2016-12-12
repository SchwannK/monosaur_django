from django.db import models

from monosaur.models import Category
from subscriptions.models import Subscription


class Session(models.Model):
    session_id = models.CharField(max_length=40, null=True)
    last_read = models.DateTimeField(null=True)
    
    def __str__(self):
        return "Session(" + ", ".join(["session_id=" + self.session_id, "last_read=" + str(self.last_read)]) + ")"
    
class Transaction(models.Model):
    name = models.CharField(max_length=100)
    amount = models.FloatField()
    date = models.DateField()
    category = models.ForeignKey(Category)
    subscription = models.ForeignKey(
        Subscription, null=True, blank=True
    )
    session = models.ForeignKey(Session)
    
    class Meta:
        unique_together = (('name', 'amount', 'date', 'session'),)
    
    def __str__(self):
        return "Transaction(" + ", ".join(["name=" + self.name, "amount=" + str(self.amount) + "GBP", "date=" + str(self.date), \
                                           "category=" + str(self.category), "subscription=" + str(self.subscription)]) + ")"
