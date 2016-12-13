from django.conf.urls import url

from . import views_admin


urlpatterns = [
    url(r'^cleanup/', views_admin.database_cleanup, name='spend_analyser'),
    url(r'^clear/', views_admin.database_clear, name='spend_analyser'),
    url(r'^test/', views_admin.database_test, name='spend_analyser'),
]
