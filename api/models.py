import datetime

from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    password = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.user


class HighSchool(models.Model):
    name = models.CharField(max_length=500)
    abbreviation = models.CharField(max_length=100)
    manager = models.OneToOneField(
        User, on_delete=models.SET_NULL, null=True, blank=True
    )
    faculties = models.ManyToManyField("Faculty", blank=True)
    departments = models.ManyToManyField("Department", blank=True)
    specializations = models.ManyToManyField("Specialization", blank=True)
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Faculty(models.Model):
    name = models.CharField(max_length=500)
    abbreviation = models.CharField(max_length=100)
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Department(models.Model):
    name = models.CharField(max_length=500)
    abbreviation = models.CharField(max_length=100)
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Classificator(models.Model):
    name = models.CharField(max_length=500)

    def __str__(self):
        return self.name


class Degree(models.Model):
    name = models.CharField(max_length=100)
    duration = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(7)]
    )

    def __str__(self):
        return f"{self.name} ({self.duration} ýyl)"


class Specialization(models.Model):

    name = models.CharField(max_length=500)
    abbreviation = models.CharField(max_length=100)
    classificator = models.ForeignKey(
        "Classificator", on_delete=models.SET_NULL, null=True, blank=True
    )
    active = models.BooleanField(default=False)
    degree = models.ForeignKey(
        "Degree", on_delete=models.SET_NULL, null=True, blank=True
    )

    def __str__(self):
        return self.name


class Student(models.Model):
    class Gender(models.TextChoices):
        MALE = "M", "Oglan"
        FEMALE = "F", "Gyz"

    class FamilyStatus(models.TextChoices):
        FOSTER = "FR", "Hossarly"
        HALF_ORPHAN = "HO", "Ýarym ýetim"
        COMPLETE_ORPHAN = "CO", "Doly ýetim"
        ORPHANAGE = "OE", "Ýetimler öýünde ösen"

    class PaymentType(models.TextChoices):
        PAID = "P", "Tölegli"
        BUDGET = "B", "Býudjet"

    full_name = models.CharField(max_length=400)
    gender = models.CharField(max_length=1, choices=Gender.choices)
    family_status = models.CharField(max_length=2, choices=FamilyStatus.choices)
    payment_type = models.CharField(max_length=1, choices=PaymentType.choices)
    high_school = models.ForeignKey("HighSchool", on_delete=models.SET_NULL, null=True)
    nationality = models.ForeignKey(
        "Nationality", on_delete=models.SET_NULL, null=True, blank=True
    )
    country = models.ForeignKey(
        "Country", on_delete=models.SET_NULL, null=True, blank=True
    )
    region = models.ForeignKey(
        "Region", on_delete=models.SET_NULL, null=True, blank=True
    )
    specialization = models.ForeignKey(
        "Specialization", on_delete=models.SET_NULL, null=True, blank=True
    )
    birth_date = models.DateField(default=datetime.date(1970, 1, 1))
    admission_date = models.DateField()
    registered_place = models.TextField()
    phone_number = models.CharField(max_length=20)
    passport = models.CharField(max_length=20)
    military_service = models.CharField(max_length=20, blank=True, null=True)
    label = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.full_name}"


class Nationality(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]


class Country(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]


class Region(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
