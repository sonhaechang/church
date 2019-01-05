from django.conf import settings
from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    baptism = models.CharField(max_length=20, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    birthday = models.CharField(max_length=8, blank=True)


    def __str__(self):
        return self.user.username
