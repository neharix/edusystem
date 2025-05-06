from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import EducationCenter


# Resources
class EducationCenterResource(resources.ModelResource):

    class Meta:
        model = EducationCenter  # or 'core.Book'


# Register your models here.
@admin.register(EducationCenter)
class EducationCenterAdmin(ImportExportModelAdmin):
    list_display = ["name", "phone_number", "address", "is_active", "id"]
    search_fields = ["name", "phone_number", "address", "region"]
    readonly_fields = ("id",)
    resource_classes = [EducationCenterResource]
