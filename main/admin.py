from django.contrib import admin
from unfold.admin import ModelAdmin as UnfoldModelAdmin

from .models import *


@admin.register(Profile)
class ProfileAdmin(UnfoldModelAdmin):
    list_display = ["user", "id", "password", "allowed_service", "otp"]
    readonly_fields = ("id",)
    search_fields = ["user", "password", "allowed_service", "otp"]


@admin.register(Country)
class CountryAdmin(UnfoldModelAdmin):
    list_display = ["name", "id"]
    readonly_fields = ("id",)
    search_fields = ["name"]


@admin.register(Region)
class RegionAdmin(UnfoldModelAdmin):
    list_display = ["name", "id"]
    readonly_fields = ("id",)
    search_fields = ["name"]


@admin.register(Nationality)
class NationalityAdmin(UnfoldModelAdmin):
    list_display = ["name", "id"]
    readonly_fields = ("id",)
    search_fields = ["name"]
