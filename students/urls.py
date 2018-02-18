from django.conf.urls import url

from . import views

# Register the namespace
app_name = 'students'

urlpatterns = [
    url(r'^$', views.profile, name='profile'),
    url(r'^signup/$', views.signup, name='signup'),
]
