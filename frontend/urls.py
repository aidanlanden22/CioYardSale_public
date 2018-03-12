from django.conf.urls import url

from . import views

# Register the namespace
app_name = 'frontend'

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^sell/$', views.sellItem, name='sellItem'),
	# url(r'^$', views.CioProfile, name='profile'),
]
