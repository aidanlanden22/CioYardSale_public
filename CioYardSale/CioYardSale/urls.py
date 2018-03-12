from django.conf.urls import url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
	url(r'^api/v1/commodity/', include('api.commodity.urls')),
	url(r'^api/v1/experience/', include('experience.urls')),
]
