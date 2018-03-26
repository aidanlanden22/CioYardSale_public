from django.db import models
from django.utils import timezone

# Create your models here.
class myUser(models.Model):
    username = models.CharField(max_length=30, unique=True, default=None)
    password = models.CharField(max_length=100, default=None)

    def __str__(self):
        return self.username


class Authenticater():
    myUser = models.ForeignKey(myUser)
    authenticator = models.CharField(max_length=100,primary_key=True)
    date_created = models.DateTimeField(default=timezone.now)