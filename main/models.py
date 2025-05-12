import random
from string import ascii_lowercase

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


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


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    password = models.CharField(max_length=200, null=True, blank=True)
    ALLOWED_SERVICES = [
        ("bmdu", "BMDU"),
        ("mmu", "MMU"),
        ("both", "Both Services"),
        ("none", "None of them"),
    ]
    allowed_service = models.CharField(
        max_length=20, choices=ALLOWED_SERVICES, default="none"
    )
    otp = models.CharField(max_length=5, null=True, blank=True, default=None)
    role = models.CharField(max_length=100, default="default")
    temp_key = models.CharField(max_length=50, null=True, blank=True)

    def generate_otp(self, *args, **kwargs):
        characters = ascii_lowercase + "1234567890"
        self.temp_key = "".join(
            [random.choice(characters) for i in range(random.randint(10, 49))]
        )
        self.otp = str(random.randint(10000, 99999))
        self.save()

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
