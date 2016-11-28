from django.db import models
from django.utils import timezone

# Create your models here.

class Transaction(models.Model):
    name = models.CharField(max_length=100)
    amount = models.FloatField()
    date = models.DateField()
    classification = models.CharField(max_length=100)

    def __str__(self):
        return self.name
