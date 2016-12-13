from django.db import models

from monosaur import fixture_utils


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

class FixtureCompany(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)
    reference = models.CharField(max_length=100, unique=True)
    category = models.ForeignKey(Category, null=True, blank=True)

    def __str__(self):
        return self.name
    
    @staticmethod
    def dump():
        fixture_utils.create_fixture('monosaur.FixtureCompany', 'monosaur/fixtures/fixture_company.json')