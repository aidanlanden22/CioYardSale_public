from django.contrib import admin

# Register your models here.
from . import models

admin.site.register(models.myUser)
admin.site.register(models.Authenticater)
