from django.conf.urls import url
from frontend import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^view_item/(?P<pk>\d+)/$', views.view_item, name='view_item'),
    url(r'^signup/$', views.register_student, name='register_student'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
]
