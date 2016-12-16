from django.db import models

from monosaur.models import Company
from monosaur.utils import fixture_utils


class Subscription(models.Model):
    name = models.CharField(max_length=200)
    company = models.ForeignKey(Company, null=True)
    description = models.TextField()
    monthly_price = models.FloatField()
    subscription_url = models.CharField(max_length=200)
    reference = models.CharField(max_length=100)

    def __str__(self):
        return self.reference

    @staticmethod
    def save_to_fixture():
        fixture_utils.create_fixture('monosaur.Company', 'subscriptions/fixtures/subscriptions_db.json')    
    
    @staticmethod
    def load_from_fixture():
        Company.objects.all().delete()
        fixture_utils.import_fixture('subscriptions/fixtures/subscriptions_db.json')
