from django.conf.urls import url

from . import views

# Register the namespace
app_name = 'experience'

urlpatterns = [
	url(r'^getCommodityList/$', views.getCommodityList, name='getCommodityList'),
]
