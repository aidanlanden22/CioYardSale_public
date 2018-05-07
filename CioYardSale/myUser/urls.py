from django.conf.urls import url, include
from . import views

# Register the namespace
app_name = 'myUser'

urlpatterns = [
    url(r'^login/$', views.login, name='login'),
    url(r'^create/$', views.create_auth, name='create_auth'),
    url(r'^create_user/$', views.create_user, name='create_user'),
    url(r'^readAll/$', views.readAll, name='readAll'),
    url(r'^getUsername/$', views.get_username, name='getUsername'),
    url(r'^delete_auth/$', views.delete_auth, name='delete_auth'),
]
