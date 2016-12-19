from django.contrib import admin

from monosaur.models import Category, Company, Uncategorised


myModels = [Category, Company, Uncategorised]

admin.site.register(myModels)

