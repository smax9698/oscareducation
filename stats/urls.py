from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.dashboard, name='dashboard'),
    url(r'^statistics/student/(?P<student>[a-zAZ0-9]+)', views.dashboard, name='dashboard'),
    url(r'^statistics/classroom/(?P<class>[a-zA-Z0-9]+)', views.dashboard, name='dashboard'),
]
