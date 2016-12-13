from django.contrib import admin

from monosaur.models import Category, Company, FixtureCompany


myModels = [Category, Company, FixtureCompany]

admin.site.register(myModels)

