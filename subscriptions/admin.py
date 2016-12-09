from django.contrib import admin

from subscriptions.models import Subscription


myModels = [Subscription]

admin.site.register(myModels)

