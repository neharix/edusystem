from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import (
    Achievement,
    Certificate,
    Country,
    Course,
    Direction,
    EducationCenter,
    File,
    Nationality,
    Region,
    Specialization,
    Staff,
    Student,
)
from .resources import (
    AchievementResource,
    Certificate,
    CertificateResource,
    CourseResource,
    DirectionResource,
    EducationCenterResource,
    FileResource,
    SpecializationResource,
    StaffResource,
    StudentResource,
)


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


@admin.register(EducationCenter)
class EducationCenterAdmin(ImportExportModelAdmin):
    list_display = [
        "name",
        "phone_number",
        "address",
        "is_active",
        "id",
        "region",
        "country",
    ]
    search_fields = ["name", "phone_number", "address"]
    list_filter = ["region", "country", "is_active"]
    filter_horizontal = ["workers", "staff"]
    readonly_fields = ("id",)
    resource_classes = [EducationCenterResource]


@admin.register(File)
class FileAdmin(ImportExportModelAdmin):
    list_display = ["name", "id", "content", "uploader", "to", "to_storage"]
    search_fields = ["name", "content"]
    list_filter = ["is_active"]
    readonly_fields = ("id",)
    resource_classes = [FileResource]


@admin.register(Staff)
class StaffAdmin(ImportExportModelAdmin):
    list_display = [
        "full_name",
        "id",
        "place_of_residence",
        "phone_number",
        "education_degree",
        "region",
        "country",
    ]
    search_fields = [
        "full_name",
        "place_of_residence",
        "phone_number",
        "education_degree",
    ]
    list_filter = ["education_degree", "region", "country"]
    filter_vertical = ["specializations"]
    readonly_fields = ("id",)
    resource_classes = [StaffResource]


@admin.register(Specialization)
class SpecializationAdmin(ImportExportModelAdmin):
    list_display = ["name", "id"]
    search_fields = ["name"]
    readonly_fields = ("id",)
    resource_classes = [SpecializationResource]


@admin.register(Achievement)
class AchievementAdmin(ImportExportModelAdmin):
    list_display = ["name", "id"]
    search_fields = ["name"]
    readonly_fields = ("id",)
    resource_classes = [AchievementResource]


@admin.register(Direction)
class DirectionAdmin(ImportExportModelAdmin):
    list_display = ["name", "id"]
    search_fields = ["name"]
    readonly_fields = ("id",)
    resource_classes = [DirectionResource]


@admin.register(Course)
class CourseAdmin(ImportExportModelAdmin):
    list_display = ["name", "id"]
    search_fields = ["name"]
    readonly_fields = ("id",)
    resource_classes = [CourseResource]


@admin.register(Certificate)
class CertificateAdmin(ImportExportModelAdmin):
    list_display = ["student", "education_center"]
    readonly_fields = ("id",)
    resource_classes = [CertificateResource]


@admin.register(Student)
class StudentAdmin(ImportExportModelAdmin):
    list_display = [
        "full_name",
        "phone_number",
        "id",
        "region",
        "country",
    ]
    search_fields = ["full_name", "phone_number", "place_of_residence"]
    list_filter = ["region", "country", "nationality"]
    readonly_fields = ("id",)
    resource_classes = [StudentResource]
