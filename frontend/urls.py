from django.conf.urls import url, include

from . import views

# Register the namespace
app_name = 'frontend'

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^sell/$', views.sellItem, name='sellItem'),
	url(r'^api/v1/commodity/', include('api.commodity.urls')),
]
