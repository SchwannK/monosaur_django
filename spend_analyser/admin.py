from django.contrib import admin

from spend_analyser.models import Transaction


myModels = [Transaction]

admin.site.register(myModels)
