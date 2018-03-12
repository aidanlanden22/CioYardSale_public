from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
	url(r'^api/v1/commodity/', include('commodity.urls')),
	url(r'^api/v1/students/', include('students.urls')),
    url(r'^api/v1/cio/', include('cio.urls')),
]
