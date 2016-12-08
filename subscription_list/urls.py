from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.subscription_list, name='subscription_list')
]
