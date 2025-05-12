from django.contrib import admin

from .models import *


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "id", "password", "allowed_service", "otp"]
    readonly_fields = ("id",)
    search_fields = ["user", "password", "allowed_service", "otp"]


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ["name", "id"]
    readonly_fields = ("id",)
    search_fields = ["name"]


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ["name", "id"]
    readonly_fields = ("id",)
    search_fields = ["name"]


@admin.register(Nationality)
class NationalityAdmin(admin.ModelAdmin):
    list_display = ["name", "id"]
    readonly_fields = ("id",)
    search_fields = ["name"]
