from django.db import models

from monosaur.utils import fixture_utils
from unicodedata import category


class EmptyStringToNoneField(models.CharField):
    def get_prep_value(self, value):
        if value == '':
            return None  
        return value

class EmptyForeignKeyToNoneField(models.ForeignKey):
    def get_prep_value(self, value):
        if not value:
            return None  
        return value

# Spending categories. Income categories are included too.
class Category(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name

# One company can have many subscriptions (see subscriptions.Subscription)
class Company(models.Model):
    name = EmptyStringToNoneField(max_length=50, null=True, blank=True)
    reference = models.CharField(max_length=100, unique=True)
    category = EmptyForeignKeyToNoneField(Category, null=True, blank=True)

    def __str__(self):
        return self.name or ("c'" + str(self.reference) + "'")
    
    @staticmethod
    def save_to_fixture():
        fixture_utils.create_fixture('monosaur.Company', 'monosaur/fixtures/company_db.json')    
    
    @staticmethod
    def load_from_fixture():
        Company.objects.all().delete()
        fixture_utils.import_fixture('monosaur/fixtures/company_db.json')
        
    @staticmethod
    def search_by_reference(reference):
        # Not the best solution as it's specific to SQLite. And the point of querysets is to be abstracted from the concrete db implementation. But it's ok for now
        companies = Company.objects.raw("SELECT * FROM monosaur_company where %s LIKE '%%' || reference || '%%'", [reference])[:1]
        
        if companies:
            return companies[0]
        else:
            return None

# This table is used to categorise uploaded transactions.
class Uncategorised(models.Model):
    name = EmptyStringToNoneField(max_length=50, null=True, blank=True)
    reference = models.CharField(max_length=100, unique=True)
    category = EmptyForeignKeyToNoneField(Category, null=True, blank=True)

    def __str__(self):
        return self.name or ("u'" + str(self.reference) + "'")
    
    @staticmethod
    def save_to_fixture():
        fixture_utils.create_fixture('monosaur.Uncategorised', 'monosaur/fixtures/uncategorised_db.json')    
    
    @staticmethod
    def load_from_fixture():
        Uncategorised.objects.all().delete()
        fixture_utils.import_fixture('monosaur/fixtures/uncategorised_db.json')

    def all_set(self):
        return self.name != None and self.reference != None and self.category != None