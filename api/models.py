import datetime

from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    password = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.user.username


class HighSchool(models.Model):
    name = models.CharField(max_length=500)
    abbreviation = models.CharField(max_length=100)
    manager = models.OneToOneField(
        Profile, on_delete=models.SET_NULL, null=True, blank=True
    )
    active = models.BooleanField(default=False)
    lat = models.FloatField(blank=True, default=37.95)
    lng = models.FloatField(blank=True, default=58.38)

    def __str__(self):
        return self.name


class Faculty(models.Model):
    name = models.CharField(max_length=500)
    abbreviation = models.CharField(max_length=100)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class HighSchoolFaculty(models.Model):
    high_school = models.ForeignKey("HighSchool", on_delete=models.CASCADE)
    faculty = models.ForeignKey("Faculty", on_delete=models.CASCADE)

    def __str__(self):
        return self.faculty.name


class Department(models.Model):
    name = models.CharField(max_length=500)
    abbreviation = models.CharField(max_length=100)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class FacultyDepartment(models.Model):
    high_school_faculty = models.ForeignKey(
        "HighSchoolFaculty", on_delete=models.CASCADE
    )
    department = models.ForeignKey("Department", on_delete=models.CASCADE)

    def __str__(self):
        return self.department.name


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
    active = models.BooleanField(default=True)
    degree = models.ForeignKey(
        "Degree", on_delete=models.SET_NULL, null=True, blank=True
    )

    def __str__(self):
        return self.name


class DepartmentSpecialization(models.Model):
    faculty_department = models.ForeignKey(
        "FacultyDepartment", on_delete=models.CASCADE
    )
    specialization = models.ForeignKey("Specialization", on_delete=models.CASCADE)

    def __str__(self):
        return self.specialization.name


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
        "DepartmentSpecialization", on_delete=models.SET_NULL, null=True, blank=True
    )
    birth_date = models.DateField(default=datetime.date(1970, 1, 1))
    admission_date = models.DateField()
    registered_place = models.TextField()
    study_year = models.IntegerField(default=1)
    phone_number = models.CharField(max_length=20)
    passport = models.CharField(max_length=20)
    military_service = models.CharField(max_length=20, blank=True, null=True)
    label = models.TextField(null=True, blank=True)
    active = models.BooleanField(default=True)
    is_expelled = models.BooleanField(default=False)

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


class ExpulsionReason(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]


class ExpulsionRequest(models.Model):
    class Verdict(models.TextChoices):
        CONFIRMED = "C", "Confirmed"
        REJECTED = "R", "Rejected"

    sender = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="expulsion_request_sender",
    )
    reason = models.ForeignKey("ExpulsionReason", on_delete=models.SET_NULL, null=True)
    student = models.ForeignKey("Student", on_delete=models.CASCADE)
    detail = models.TextField()
    request_date = models.DateTimeField(auto_now_add=True)
    verdict_date = models.DateTimeField(null=True, blank=True)
    verdict = models.CharField(
        max_length=1, choices=Verdict.choices, null=True, blank=True
    )
    viewed_by = models.ManyToManyField(User, blank=True)
    is_obsolete = models.BooleanField(default=False)

    def confirm(self, *args, **kwargs):
        self.verdict = "C"
        self.student.is_expelled = True
        self.student.save()
        for reinstate_request in ReinstateRequest.objects.filter(student=self.student):
            reinstate_request.is_obsolete = True
            reinstate_request.save()
        self.verdict_date = timezone.now()
        self.save()

    def reject(self, *args, **kwargs):
        self.verdict = "R"
        self.verdict_date = timezone.now()
        self.save()

    def __str__(self):
        return f"{self.student.full_name} {self.request_date} {self.verdict}"

    class Meta:
        ordering = ["verdict_date"]


class ReinstateRequest(models.Model):
    class Verdict(models.TextChoices):
        CONFIRMED = "C", "Confirmed"
        REJECTED = "R", "Rejected"

    sender = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="reinstate_request_sender",
    )
    student = models.ForeignKey("Student", on_delete=models.CASCADE)
    detail = models.TextField()
    request_date = models.DateTimeField(auto_now_add=True)
    verdict_date = models.DateTimeField(null=True, blank=True)
    verdict = models.CharField(
        max_length=1, choices=Verdict.choices, null=True, blank=True
    )
    viewed_by = models.ManyToManyField(User, blank=True)
    is_obsolete = models.BooleanField(default=False)

    def confirm(self, *args, **kwargs):
        self.verdict = "C"
        self.student.is_expelled = False
        self.student.save()
        for expulsion_request in ExpulsionRequest.objects.filter(student=self.student):
            expulsion_request.is_obsolete = True
            expulsion_request.save()

        self.verdict_date = timezone.now()
        self.save()

    def reject(self, *args, **kwargs):
        self.verdict = "R"
        self.verdict_date = timezone.now()
        self.save()

    def __str__(self):
        return f"{self.student.full_name} {self.request_date} {self.verdict}"

    class Meta:
        ordering = ["verdict_date"]


class DiplomaRequest(models.Model):
    class Verdict(models.TextChoices):
        CONFIRMED = "C", "Confirmed"
        REJECTED = "R", "Rejected"

    sender = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="diploma_request_sender",
    )
    simple_diploma_count = models.PositiveIntegerField(default=0)
    honor_diploma_count = models.PositiveIntegerField(default=0)
    request_date = models.DateTimeField(auto_now_add=True)
    verdict_date = models.DateTimeField(null=True, blank=True)
    verdict = models.CharField(
        max_length=1, choices=Verdict.choices, null=True, blank=True
    )
    allowed_until = models.DateTimeField(
        default=timezone.now() + datetime.timedelta(days=30)
    )
    viewed_by = models.ManyToManyField(User, blank=True)
    is_obsolete = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.sender} {self.request_date}"


class DiplomaRequestAction(models.Model):
    class Verdict(models.TextChoices):
        CONFIRMED = "C", "Confirmed"

    update_simple_to = models.PositiveIntegerField(default=0)
    update_honor_to = models.PositiveIntegerField(default=0)
    diploma_request = models.ForeignKey("DiplomaRequest", on_delete=models.CASCADE)
    request_date = models.DateTimeField(auto_now_add=True)
    verdict_date = models.DateTimeField(null=True, blank=True)
    verdict = models.CharField(
        max_length=1, choices=Verdict.choices, null=True, blank=True
    )

    def update_diploma_request(self, *args, **kwargs):
        self.diploma_request.viewed_by.clear()
        self.diploma_request.save()

    def __str__(self):
        return f"{self.diploma_request} {self.request_date}"

    class Meta:
        ordering = ["-verdict_date"]


class DiplomaReport(models.Model):
    class Verdict(models.TextChoices):
        CONFIRMED = "C", "Confirmed"

    diploma_request = models.ForeignKey("DiplomaRequest", on_delete=models.CASCADE)
    two_year_work_off = models.PositiveIntegerField(default=0)
    died = models.PositiveIntegerField(default=0)
    went_abroad = models.PositiveIntegerField(default=0)
    other_reasons = models.PositiveIntegerField(default=0)
    request_date = models.DateTimeField(auto_now_add=True)
    verdict_date = models.DateTimeField(null=True, blank=True)
    verdict = models.CharField(
        max_length=1, choices=Verdict.choices, null=True, blank=True
    )

    def update_diploma_request(self, *args, **kwargs):
        self.diploma_request.viewed_by.clear()
        self.diploma_request.save()

    def __str__(self):
        return f"{self.diploma_request} {self.request_date}"

    class Meta:
        ordering = ["-verdict_date"]


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
