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
    # path("specializations/", specialization_list_create_view),
]
