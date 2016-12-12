from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.spend_analyser, name='spend_analyser'),
    url(r'^cleanup/', views.database_cleanup, name='spend_analyser')
]
