from django.db import models

from api.models import Country, Region


# Create your models here.
class EducationCenter(models.Model):
    name = models.CharField(max_length=500)
    phone_number = models.CharField(max_length=150)
    lat = models.FloatField(blank=True, null=True)
    lng = models.FloatField(blank=True, null=True)

    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True)
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True)
    address = models.TextField(null=True, blank=True)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
