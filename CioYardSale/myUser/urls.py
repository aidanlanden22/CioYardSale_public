from django.conf.urls import url, include
from . import views

# Register the namespace
app_name = 'myUser'

urlpatterns = [
    url(r'^login/$', views.login, name='login'),
    url(r'^create/$', views.create_auth, name='create_auth'),
]
