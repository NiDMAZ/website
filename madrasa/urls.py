from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.homepage, name='homepage'),
    url(r'students$', views.students, name='students'),
    url(r'classes$', views.madrasa_classes, name='classes'),
]
