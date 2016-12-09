from django.contrib import admin

from monosaur.models import Category, Company


myModels = [Category, Company]

admin.site.register(myModels)

