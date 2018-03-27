from django.conf.urls import url, include
from . import views

# Register the namespace
app_name = 'myUser'

urlpatterns = [
    url(r'^login/$', views.login, name='login'),
    url(r'^create/$', views.create_auth, name='create_auth'),
<<<<<<< HEAD
    url(r'^create_user/$', views.create_user, name='create_user'),
    url(r'^readAll/$', views.readAll, name='readAll'),
=======
>>>>>>> 0cd7ddec6249b68ca2462b19dfa6f55b42765e5e
]
