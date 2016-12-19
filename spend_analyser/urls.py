from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.spend_analyser, name='spend_analyser'),
    url(r'^print_to_pdf/', views.print_to_pdf),
    url(r'^(?P<session_id>[-\w\d]+)/', views.spend_analyser),
]
