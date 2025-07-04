from django.contrib import admin

from .models import *


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

@admin.register(AnnualUpdateReport)
class AnnualUpdateReportAdmin(admin.ModelAdmin):
    list_display = ["updated_at", "id"]
    readonly_fields = ("id",)


@admin.register(HighSchool)
class HighSchoolAdmin(admin.ModelAdmin):
    list_display = ["name", "id", "abbreviation", "active"]
    readonly_fields = ("id",)
    search_fields = ["name", "abbreviation"]


@admin.register(HighSchoolFaculty)
class HighSchoolFacultyAdmin(admin.ModelAdmin):
    list_display = ["high_school", "faculty", "id"]
    readonly_fields = ("id",)


@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = ["name", "id", "abbreviation", "active"]
    readonly_fields = ("id",)
    search_fields = ["name", "abbreviation"]


@admin.register(FacultyDepartment)
class FacultyDepartmentAdmin(admin.ModelAdmin):
    list_display = ["high_school_faculty", "department", "id"]
    readonly_fields = ("id",)


@admin.register(DepartmentSpecialization)
class DepartmentSpecializationAdmin(admin.ModelAdmin):
    list_display = ["faculty_department", "specialization", "shell_name", "id"]
    readonly_fields = ("id",)


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ["name", "id", "abbreviation", "active"]
    readonly_fields = ("id",)
    search_fields = ["name", "abbreviation"]


@admin.register(Specialization)
class SpecializationAdmin(admin.ModelAdmin):
    list_display = ["name", "id", "abbreviation", "active"]
    readonly_fields = ("id",)
    search_fields = ["name", "abbreviation"]


@admin.register(Classificator)
class ClassificatorAdmin(admin.ModelAdmin):
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
    list_display = ["full_name", "birth_date", "admission_date", "high_school", "id"]
    search_fields = ["full_name", "phone_number", "passport", "registered_place"]
    list_filter = [
        "gender",
        "family_status",
        "payment_type",
        "high_school",
        "nationality",
        "country",
        "region",
        "is_expelled",
        "is_obsolete",
        "active",
    ]


@admin.register(ExpulsionReason)
class ExpulsionReasonAdmin(admin.ModelAdmin):
    list_display = ["name", "id"]
    readonly_fields = ("id",)
    search_fields = ["name"]


@admin.register(ExpulsionRequest)
class ExpulsionRequestAdmin(admin.ModelAdmin):
    list_display = ["student", "request_date", "verdict_date", "verdict", "id"]
    readonly_fields = ("request_date", "verdict_date", "id")


@admin.register(ReinstateRequest)
class ReinstateRequestAdmin(admin.ModelAdmin):
    list_display = ["student", "request_date", "verdict_date", "verdict", "id"]
    readonly_fields = ("request_date", "verdict_date", "id")


@admin.register(DiplomaRequest)
class DiplomaRequestAdmin(admin.ModelAdmin):
    list_display = ["sender", "request_date", "is_obsolete", "id", "allowed_until"]
    list_editable = ["allowed_until"]
    readonly_fields = ("request_date", "verdict_date", "id")


@admin.register(DiplomaRequestAction)
class DiplomaRequestActionAdmin(admin.ModelAdmin):
    list_display = [
        "diploma_request",
        "update_simple_to",
        "update_honor_to",
        "request_date",
        "id",
    ]
    readonly_fields = ("request_date", "id")


@admin.register(DiplomaReport)
class DiplomaReportAdmin(admin.ModelAdmin):
    list_display = ["diploma_request", "request_date", "id"]
    readonly_fields = ("request_date", "id")


@admin.register(TeacherStatement)
class TeacherStatementAdmin(admin.ModelAdmin):
    list_display = ["sender", "request_date", "is_obsolete", "id", "allowed_until"]
    list_editable = ["allowed_until"]
    readonly_fields = ("request_date", "verdict_date", "id")
