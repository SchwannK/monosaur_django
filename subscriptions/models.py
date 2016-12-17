from django.db import models

from monosaur.models import Company
from monosaur.utils import fixture_utils


class Subscription(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    company = models.ForeignKey(Company)
    description = models.TextField(null=True, blank=True)
    monthly_price = models.FloatField(null=True, blank=True)
    subscription_url = models.CharField(max_length=200, null=True, blank=True)
    reference = models.CharField(max_length=100)

    def __str__(self):
        return self.name or self.reference

    @staticmethod
    def save_to_fixture():
        fixture_utils.create_fixture('monosaur.Company', 'subscriptions/fixtures/subscriptions_db.json')    
    
    @staticmethod
    def load_from_fixture():
        Company.objects.all().delete()
        fixture_utils.import_fixture('subscriptions/fixtures/subscriptions_db.json')
