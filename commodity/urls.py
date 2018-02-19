from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.sell, name='sell'),
    url(r'^create/$', views.create, name='create'),
    
    
    url(r'^(?P<pk>[0-9]+)/$', views.read, name='read'),
    
]
