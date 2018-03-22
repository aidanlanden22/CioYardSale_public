from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Cio(models.Model):
    username = models.CharField(max_length=30, unique=True, default=None)
    password = models.CharField(max_length=100,default=None)

class Authenticator(models.Model):
	user = models.ForeignKey(Cio)
	authenticator = models.CharField(max_length=100, primary_key=True)
	timestamp = models.DateTimeField(default=timezone.now)
