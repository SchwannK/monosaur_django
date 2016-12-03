from django.contrib import admin
from .models import Transaction, Category, Company

# Register your models here.

myModels = [Transaction, Category, Company]

admin.site.register(myModels)
