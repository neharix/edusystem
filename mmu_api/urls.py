from django.contrib import admin
from django.urls import path

from main.views import CustomTokenObtainPairView

from .views import *

urlpatterns = [
    # path("/", view, name=""),
    # Authentication routes
    path("token/", CustomTokenObtainPairView.as_view(), name="token-obtain-pair"),
    path("user/", get_user_data, name="user-data"),
    path("try-otp/", try_otp_api_view, name="otp"),
    path("check-otp/", check_otp_api_view, name="check-otp"),
    path(
        "change-password/",
        change_password_api_view,
        name="change-password-api-view",
    ),
    # Special routes
    path("dashboard/", dashboard_api_view),
    path("service-toggler/", toggle_service_status),
    path("delete/", delete_data),
    path("export/", export_data),
    path("import/", import_data),
    # Profile routes
    path("profiles/", profile_list_view, name="profile-list"),
    # Education center routes
    path(
        "education-centers/",
        education_center_list_create_view,
        name="education-center-list-create",
    ),
    path(
        "education-centers/<int:education_center_id>/",
        education_center_retrieve_update_delete_view,
        name="education-center-retrieve-update-delete",
    ),
    path(
        "about-education-center/<int:education_center_id>/",
        about_education_center,
        name="about-education-center",
    ),
    path(
        "education-centers/<int:education_center_id>/files/",
        get_education_center_files,
        name="education-center-files-list",
    ),
    path(
        "education-centers/<int:education_center_id>/staff/",
        get_education_center_staff,
        name="education-center-staff-list",
    ),
    # Region routes
    path("regions/", region_list_view, name="region-list"),
    # Nationality routes
    path("nationalities/", nationality_list_view, name="nationality-list"),
    # Country routes
    path("countries/", country_list_view, name="country-list"),
    # Achievement routes
    path("achievements/", achievement_list_create_view, name="achievement-list-create"),
    path(
        "achievements/<int:achievement_id>/",
        achievement_retrieve_update_delete_view,
        name="achievement-retrieve-update-delete",
    ),
    # File routes
    path("download/<int:file_id>/", download_file),
    path(
        "files/",
        file_list_create_view,
        name="file-retrieve-delete-view",
    ),
    path(
        "files/<int:file_id>/",
        file_retrieve_delete_view,
        name="file-retrieve-delete-view",
    ),
    # Specialization routes
    path(
        "specializations/",
        specialization_list_create_view,
        name="specialization-list-create",
    ),
    path(
        "specializations/<int:specialization_id>/",
        specialization_retrieve_update_delete_view,
        name="specialization-retrieve-update-delete",
    ),
    # Student routes
    path(
        "students/",
        student_list_create_view,
        name="student-list-create",
    ),
    path(
        "students/<int:student_id>/",
        student_retrieve_update_delete_view,
        name="student-retrieve-update-delete",
    ),
    path(
        "students/<int:student_id>/courses/",
        get_student_courses,
        name="student-course-list",
    ),
    path(
        "students/<int:student_id>/certificates/",
        get_student_certificates,
        name="student-certificate-list",
    ),
    # Certificate routes
    path("certificates/<int:certificate_id>/", certificate_view),
]
