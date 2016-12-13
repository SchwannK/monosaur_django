from django.conf.urls import url

from . import views_admin


urlpatterns = [
    url(r'^cleanup/', views_admin.db_cleanup, name='spend_analyser'),
    url(r'^clear/', views_admin.db_clear, name='spend_analyser'),
    url(r'^test/', views_admin.test, name='spend_analyser'),
]
