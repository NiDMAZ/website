from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.homepage, name='homepage'),
    url(r'^dates$', views.current_datetime, name='current_datetime'),
    url(r'^volunteer$', views.volunteer_page, name='volunteer'),
    url(r'^blood', views.blood_drive, name='blood'),
    url(r'^display', views.display, name='display')
]
