from django.contrib import admin

from spend_analyser.models import Transaction, Session


myModels = [Transaction, Session]

admin.site.register(myModels)
