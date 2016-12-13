from django.db import models

from monosaur.utils import fixture_utils


# Spending categories. Income categories are included too.
class Category(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name

# This table is used to categorise uploaded transactions.
# A company can have many subscriptions (see subscriptions.Subscription)
class Company(models.Model):
    name = models.CharField(max_length=50)
    reference = models.CharField(max_length=100)
    category = models.ForeignKey(Category)

    def __str__(self):
        return self.name
    
    @staticmethod
    def save_to_fixture():
        fixture_utils.create_fixture('monosaur.Company', 'monosaur/fixtures/company_db.json')    
    
    @staticmethod
    def load_from_fixture():
        Company.objects.all().delete()
        fixture_utils.import_fixture('monosaur/fixtures/company_db.json')

# Previously unseen bank transaction references are dumped into this table for later categorization.
# After you finished with parsing a file (or files in case of multi-upload), don't forget to call save_to_fixture().
# Otherwise you may loose you carefully collected companies and payees at the next db reset.
class FixtureCompany(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)
    reference = models.CharField(max_length=100, unique=True)
    category = models.ForeignKey(Category, null=True, blank=True)

    def __str__(self):
        return self.reference
    
    @staticmethod
    def save_to_fixture():
        fixture_utils.create_fixture('monosaur.FixtureCompany', 'monosaur/fixtures/fixture_company.json')
        
    @staticmethod
    def load_from_fixture():
        FixtureCompany.objects.all().delete()
        fixture_utils.import_fixture('monosaur/fixtures/fixture_company.json')