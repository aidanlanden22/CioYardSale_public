from django.conf.urls import url
from frontend import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^view_item/(?P<pk>\d+)/$', views.view_item, name='view_item'),
    url(r'^signup/$', views.signup_user, name='signup_user'),
    url(r'^createlisting/$', views.create_listing, name='create_listing'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
]
