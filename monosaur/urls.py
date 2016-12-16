"""monosaur URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin, auth

from monosaur import views


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'', include('subscriptions.urls')),
    url(r'^analyse/', include('spend_analyser.urls')),
    url(r'^admin/cleanup/', views.db_cleanup),
    url(r'^admin/clear/', views.db_clear),
    url(r'^admin/company/', views.company),
    url(r'^admin/subscription/', views.subscription),
    url(r'^delete/(?P<table>[\w]+)/(?P<pk>\d+)/', views.delete, name='delete'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
