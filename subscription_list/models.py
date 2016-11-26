from django.db import models
from django.utils import timezone

# Create your models here.

class Subscription(models.Model):
    subscription_name = models.CharField(max_length=200)
    company = models.CharField(max_length=100)
    description = models.TextField()
    monthly_price = models.FloatField()
    transaction_id = models.CharField(max_length=100)
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.subscription_name
