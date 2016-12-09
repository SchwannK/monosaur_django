from django.db import models
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name
    
class Company(models.Model):
    name = models.CharField(max_length=50)
    reference = models.CharField(max_length=100)
    category = models.ForeignKey(Category)

    def __str__(self):
        return self.name

class Subscription(models.Model):
    name = models.CharField(max_length=200)
    company = models.ForeignKey(Company)
    description = models.TextField()
    monthly_price = models.FloatField()
    subscription_url = models.CharField(max_length=200)
    reference = models.CharField(max_length=100)
    created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name
