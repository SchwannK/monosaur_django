from django.db import models

from monosaur.models import Category, Company, Uncategorised
from subscriptions.models import Subscription
from .transactions.constants import DEFAULT_TRANSACTION_CATEGORY


class Session(models.Model):
    session_id = models.CharField(max_length=40, null=True)
    last_read = models.DateTimeField(null=True)
    
    def __str__(self):
        return "Session(" + ", ".join(["session_id=" + self.session_id, "last_read=" + str(self.last_read)]) + ")"

# Table for all the transactions of all the users
# Currently entries that are older than 1 day will be dumped daily by a schedule task on pythonanywhere
class Transaction(models.Model):
    name = models.CharField(max_length=100)
    amount = models.FloatField()
    date = models.DateField()
    company = models.ForeignKey(Company, on_delete=models.DO_NOTHING, null=True, blank=True)
    subscription = models.ForeignKey(
        Subscription, null=True, blank=True, on_delete=models.DO_NOTHING
    )
    session = models.ForeignKey(Session, on_delete=models.DO_NOTHING)

    @property
    def category(self):
        if self.company:
            return self.company.category
        else:
            return Category.objects.get(name=DEFAULT_TRANSACTION_CATEGORY)
    
    @property
    def uncategorised(self):
        return Uncategorised.objects.get(reference=self.name)
    
    class Meta:
        unique_together = (('name', 'amount', 'date', 'session'),)
    
    def __str__(self):
        return "Transaction(" + ", ".join(["name=" + self.name, "amount=" + str(self.amount) + "GBP", "date=" + str(self.date), \
                                           "company=" + str(self.company), "subscription=" + str(self.subscription)]) + ")"
