from django.contrib import admin

from .models import *


# Register your models here.
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "id", "password"]
    readonly_fields = ("id",)
    search_fields = ["user", "password"]


@admin.register(HighSchool)
class HighSchoolAdmin(admin.ModelAdmin):
    list_display = ["name", "id", "abbreviation", "active"]
    readonly_fields = ("id",)
    search_fields = ["name", "abbreviation"]


@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = ["name", "id", "abbreviation", "active"]
    readonly_fields = ("id",)
    search_fields = ["name", "abbreviation"]


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ["name", "id", "abbreviation", "active"]
    readonly_fields = ("id",)
    search_fields = ["name", "abbreviation"]


@admin.register(Specialization)
class SpecializationAdmin(admin.ModelAdmin):
    list_display = ["name", "id", "abbreviation", "degree", "active"]
    readonly_fields = ("id",)
    search_fields = ["name", "abbreviation"]


@admin.register(Classificator)
class ClassificatorAdmin(admin.ModelAdmin):
    list_display = ["name", "id"]
    readonly_fields = ("id",)
    search_fields = ["name"]


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


@admin.register(Degree)
class DegreeAdmin(admin.ModelAdmin):
    list_display = ["name", "duration", "id"]
    readonly_fields = ("id",)
    search_fields = ["name"]


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ["full_name"]
