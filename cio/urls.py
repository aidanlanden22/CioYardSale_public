
from django.conf.urls import url

from . import views

# Register the namespace
app_name = 'cio'

urlpatterns = [
	url(r'^$', views.profile, name='profile'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^logout/$', views.logoutUser, name='logout'),
    # API URLS
    url(r'^(?P<pk>[0-9]+)/$', views.read, name='read'),
    url(r'delete/(?P<pk>[0-9]+)/$', views.delete, name='delete'),
    url(r'update/(?P<pk>[0-9]+)/$', views.update, name='update'),
    url(r'create/(?P<pk>[0-9]+)/$', views.create, name='create'),
]