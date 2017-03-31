from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.homepage, name='homepage'),
    url(r'^dates$', views.current_datetime, name='current_datetime'),
]
