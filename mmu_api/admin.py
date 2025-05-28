from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from parler.admin import TranslatableAdmin
from unfold.admin import ModelAdmin as UnfoldModelAdmin

from .models import EducationCenter, File, Specialization, Staff
from .resources import (
    EducationCenterResource,
    FileResource,
    SpecializationResource,
    StaffResource,
)


@admin.register(EducationCenter)
class EducationCenterAdmin(UnfoldModelAdmin, ImportExportModelAdmin):
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
    filter_horizontal = ["workers", "courses", "staff"]
    readonly_fields = ("id",)
    resource_classes = [EducationCenterResource]


@admin.register(File)
class FileAdmin(UnfoldModelAdmin, ImportExportModelAdmin):
    list_display = ["name", "id", "content", "uploader", "to", "to_storage"]
    search_fields = ["name", "content"]
    list_filter = ["is_active"]
    readonly_fields = ("id",)
    resource_classes = [FileResource]


@admin.register(Staff)
class StaffAdmin(UnfoldModelAdmin, ImportExportModelAdmin):
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
class SpecializationAdmin(UnfoldModelAdmin, TranslatableAdmin, ImportExportModelAdmin):
    list_display = ["name", "id"]
    search_fields = ["name"]
    readonly_fields = ("id",)
    resource_classes = [SpecializationResource]

    def get_prepopulated_fields(self, request, obj=None):
        return {"name": ("name",)}
