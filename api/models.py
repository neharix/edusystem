import datetime

from django.contrib.auth.models import User
from django.db import models


class Degree(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Person(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    patronymic = models.CharField(max_length=100)
    degree = models.ForeignKey("Degree", on_delete=models.PROTECT)
    workplace = models.ForeignKey(
        "HighSchool", on_delete=models.PROTECT, null=True, blank=True
    )

    def __str__(self):
        return f"{self.surname} {self.name} {self.patronymic}"


class HighSchool(models.Model):
    name = models.CharField(max_length=500)
    abbreviation = models.CharField(max_length=100)
    manager = models.OneToOneField(User, on_delete=models.PROTECT)

    def __str__(self):
        return self.name


class Faculty(models.Model):
    name = models.CharField(max_length=500)
    abbreviation = models.CharField(max_length=100)
    high_school = models.ForeignKey("HighSchool", on_delete=models.PROTECT)
    dean = models.OneToOneField(
        "Person", on_delete=models.PROTECT, related_name="faculty_dean"
    )
    deputy_deans = models.ManyToManyField("Person")

    def __str__(self):
        return self.name


class Department(models.Model):
    name = models.CharField(max_length=500)
    abbreviation = models.CharField(max_length=100)
    director = models.OneToOneField("Person", on_delete=models.PROTECT)
    faculty = models.ForeignKey("Faculty", on_delete=models.PROTECT)

    def __str__(self):
        return self.name


class SpecializationSeed(models.Model):
    name = models.CharField(max_length=500)
    abbreviation = models.CharField(max_length=100)
    department = models.ForeignKey("Department", on_delete=models.PROTECT)

    def __str__(self):
        return self.name


class Specialization(models.Model):
    seed = models.ForeignKey("SpecializationSeed", on_delete=models.PROTECT)
    year = models.IntegerField(default=1)
    index = models.IntegerField(blank=True, null=True)
    curator = models.OneToOneField("Person", on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.year} {self.seed.name} {self.index}"


class Student(models.Model):
    class Gender(models.TextChoices):
        MALE = "M", "Erkek"
        FEMALE = "F", "Gyz"

    class FamilyStatus(models.TextChoices):
        pass

    class PaymentType(models.TextChoices):
        pass

    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    patronymic = models.CharField(max_length=100)
    gender = models.CharField(max_length=1, choices=Gender.choices)
    family_status = models.CharField(max_length=3, choices=FamilyStatus.choices)
    payment_type = models.CharField(max_length=2, choices=PaymentType.choices)
    nationality = models.ForeignKey("Nationality", on_delete=models.PROTECT)
    country = models.ForeignKey("Country", on_delete=models.PROTECT)
    region = models.ForeignKey("Region", on_delete=models.PROTECT)
    specialization = models.ForeignKey("Specialization", on_delete=models.PROTECT)
    birth_date = models.DateField(default=datetime.date(1970, 1, 1))
    admission_type = models.DateField()
    registered_place = models.TextField()
    phone_number = models.CharField(max_length=20)
    passport = models.CharField(max_length=20)
    military_service = models.CharField(max_length=20, blank=True, null=True)
    label = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.surname} {self.name} {self.patronymic}"
