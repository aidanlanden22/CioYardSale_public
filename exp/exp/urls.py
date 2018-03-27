from django.conf.urls import url

from . import views

# Register the namespace
app_name = 'experience'

urlpatterns = [
	url(r'^getCommodityList/$', views.getCommodityList, name='getCommodityList'),
	url(r'^getSingleCommodity/(?P<pk>[0-9]+)/$', views.getSingleCommodity, name='getSingleCommodity'),
	url(r'^api/v1/login/$', views.loginUser, name='login'),
	url(r'^api/v1/logout/$', views.logoutUser, name='logout'),
	url(r'^signupUser/$', views.signupUser,name='signupUser'),
	url(r'^createComodity/$', views.createComodity, name='createComodity')
]
