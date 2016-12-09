from django.contrib import admin

from monosaur.models import Category, Company, Subscription


myModels = [Category, Company, Subscription]

admin.site.register(myModels)

