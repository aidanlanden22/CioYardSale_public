from django.db import models

# Create your models here
class Cio(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)