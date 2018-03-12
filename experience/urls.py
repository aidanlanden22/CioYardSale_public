from django.conf.urls import url

from . import views

# Register the namespace
app_name = 'experience'

urlpatterns = [
	# url(r'^$', views.sell, name='sell'),
	url(r'^$', views.profile, name='profile'),
    url(r'^signup/$', views.CIOsignup, name='signup'),
    url(r'^logout/$', views.logoutUser, name='logout'),
]
