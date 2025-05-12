from django.contrib.auth.models import User
from django.db import models

from main.models import Country, Profile, Region


# Create your models here.
class ActionLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    action = models.TextField(null=True, blank=True)
    datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} {self.datetime}"


class EducationCenter(models.Model):
    name = models.CharField(max_length=500)
    phone_number = models.CharField(max_length=150)
    lat = models.FloatField(blank=True, null=True)
    lng = models.FloatField(blank=True, null=True)

    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True)
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True)
    address = models.TextField(null=True, blank=True)

    is_active = models.BooleanField(default=True)

    personal = models.ManyToManyField(Profile, blank=True)

    def __str__(self):
        return self.name
