from django.contrib import admin

from .models import *


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "id", "password", "allowed_service", "otp"]
    readonly_fields = ("id",)
    search_fields = ["user", "password", "allowed_service", "otp"]
