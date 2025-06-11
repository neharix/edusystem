import datetime

from django.db import models

from main.models import Profile


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


# Create your models here.
class File(models.Model):
    class UserType(models.TextChoices):
        DEFAULT = "default", "default"
        WORKER = "worker", "worker"
        SUPERUSER = "superuser", "superuser"

    name = models.TextField()
    content = models.FileField(upload_to="mmu/")
    uploader = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
    to = models.ForeignKey(
        Profile,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="file_to",
    )
    to_storage = models.ForeignKey(
        "EducationCenter", on_delete=models.SET_NULL, null=True, blank=True
    )
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class ActionLog(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
    action = models.TextField(null=True, blank=True)
    datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} {self.datetime}"


class Specialization(models.Model):
    name = models.CharField(max_length=500)

    def __str__(self):
        return self.name


class Staff(models.Model):
    class EducationDegree(models.TextChoices):
        HIGH = ("high", "High")
        INCOMPLETE_HIGH = ("incompleteHigh", "Incomplete High")
        SECONDARY = ("secondary", "Secondary")
        SECONDARY_SPECIALIZED = ("specialSecondary", "Special Secondary")

    full_name = models.CharField(max_length=500)
    place_of_residence = models.TextField()
    phone_number = models.CharField(max_length=100)
    education_degree = models.CharField(max_length=20, choices=EducationDegree.choices)
    specializations = models.ManyToManyField(Specialization)

    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True)
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.full_name


class Achievement(models.Model):
    name = models.CharField(max_length=500)

    def __str__(self):
        return self.name


class Parent(models.Model):
    full_name = models.CharField(max_length=500)

    def __str__(self):
        return self.full_name


class Direction(models.Model):
    name = models.CharField(max_length=500)

    def __str__(self):
        return self.name


class Student(models.Model):
    full_name = models.CharField(max_length=500)
    nationality = models.ForeignKey(
        Nationality,
        on_delete=models.SET_NULL,
        related_name="mmu_student_nationality",
        null=True,
    )
    region = models.ForeignKey(
        Region,
        on_delete=models.SET_NULL,
        related_name="mmu_student_region",
        null=True,
    )
    country = models.ForeignKey(
        Country,
        on_delete=models.SET_NULL,
        related_name="mmu_student_country",
        null=True,
    )
    place_of_residence = models.TextField()
    phone_number = models.CharField(max_length=250)
    study_or_working_place = models.TextField()
    achievements = models.ManyToManyField(Achievement, blank=True)


class EducationCenter(models.Model):
    name = models.CharField(max_length=500)
    phone_number = models.CharField(max_length=150)

    lat = models.FloatField(blank=True, null=True)
    lng = models.FloatField(blank=True, null=True)

    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True)
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True)
    address = models.TextField(null=True, blank=True)

    is_active = models.BooleanField(default=True)

    workers = models.ManyToManyField(Profile, blank=True)
    staff = models.ManyToManyField(Staff, blank=True)

    # Material supply fields
    buildings_count = models.PositiveIntegerField(default=0)
    rooms_count = models.PositiveIntegerField(default=0)
    capacity = models.PositiveIntegerField(default=0)
    books_count = models.PositiveIntegerField(default=0)

    # Accreditation
    accreditation_file = models.ForeignKey(
        File,
        related_name="accredition_file",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )

    def __str__(self):
        return self.name

    # TODO думаю было бы неплохо создать модель учителей и добавить филд "курсы"
    # teachers = models.ManyToManyField(Teacher)


class Course(models.Model):
    education_center = models.ForeignKey(
        EducationCenter, on_delete=models.SET_NULL, null=True
    )
    name = models.CharField(max_length=500)
    students = models.ManyToManyField(Student)
    direction = models.ForeignKey(Direction, on_delete=models.SET_NULL, null=True)
    hours = models.PositiveIntegerField(default=0)
    date_start = models.DateField(null=True, blank=True)
    date_end = models.DateField(null=True, blank=True)
    lesson_time_start = models.TimeField(null=True, blank=True)
    lesson_time_end = models.TimeField(null=True, blank=True)


class Certificate(models.Model):
    student = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True)
    education_center = models.ForeignKey(
        EducationCenter, on_delete=models.SET_NULL, null=True
    )
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True)
    point = models.PositiveIntegerField(default=0)
    temp_key = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.id}.{self.student.full_name} sertifikaty"
