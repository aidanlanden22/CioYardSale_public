from django.contrib import admin
from .models import Student
# from django.contrib.auth.models import User

class StudentAdmin(admin.ModelAdmin):
    list_display = ['user_id']

admin.site.register(Student, StudentAdmin)
