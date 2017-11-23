from django.conf.urls import url

from . import views
from . import StatsObject

urlpatterns = [
    url(r'^lesson/(?P<pk>\d+)/stats/export/$', views.exportCSV, name='exportCSV'),
    url(r'^superuser/$', views.superuser_view_stats, name='superuser_view_stats'),
    url(r'^superuser/export/$', views.superuserCSV, name='superuserCSV'),
]
