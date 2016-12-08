from django.db import models
from django.utils import timezone
from ofxparse import OfxParser

from subscription_list.models import Subscription


class Category(models.Model):
    name = models.CharField(max_length=50)

class Transaction(models.Model):
    name = models.CharField(max_length=100)
    amount = models.FloatField()
    date = models.DateField()
    category = models.CharField(max_length=100)
    subscription = models.CharField(max_length=100)
    user = models.CharField(max_length=40, null=True)
    
    def __str__(self):
        return self.name

class Company(models.Model):
    name = models.CharField(max_length=50)
    reference = models.CharField(max_length=100)
    category = models.CharField(max_length=50)

    def __str__(self):
        return self.name
