from django.conf.urls import url

from . import views

# Register the namespace
app_name = 'students'

urlpatterns = [
    url(r'^(?P<pk>[0-9]+)/$', views.read, name='read'),
    url(r'^delete/(?P<pk>[0-9]+)/$', views.delete, name='delete'),
    url(r'^update/(?P<pk>[0-9]+)/$', views.update, name='update'),
    url(r'^create/$', views.create, name='create'),
]
