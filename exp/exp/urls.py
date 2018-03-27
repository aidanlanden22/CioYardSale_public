from django.conf.urls import url

from . import views

# Register the namespace
app_name = 'experience'

urlpatterns = [
	url(r'^getCommodityList/$', views.getCommodityList, name='getCommodityList'),
	url(r'^getSingleCommodity/(?P<pk>[0-9]+)/$', views.getSingleCommodity, name='getSingleCommodity'),
	url(r'^registerStudent/$', views.registerStudent,name='registerStudent'),
]
