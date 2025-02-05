from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import *

urlpatterns = [
    # Echo routes
    path("", echo),
    # Authentication routes
    path("token/", TokenObtainPairView.as_view(), name="token-obtain-pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path("user/", get_user_data, name="user-data"),
    # Special routes
    path("admin/", admin.site.urls),
    path(
        "profiles/<int:id>/", ProfileRetrieveApiView.as_view(), name="profile-retrieve"
    ),
    path(
        "get-example/high-school/<int:high_school_id>/row-count/<int:row_count>/",
        get_example,
    ),
    path("import-excel-data/", import_excel_data),
    path("dashboard/", dashboard_api_view),
    # High school routes
    path("create-high-school/", create_high_school_api_view),
    path("update-high-school/<int:high_school_id>/", put_high_school_api_view),
    path(
        "high-schools-with-additional/",
        get_high_school_with_additional_data_api_view,
        name="get-high-school-with-additional-data",
    ),
    path(
        "high-school-about/<int:high_school_id>/",
        get_high_school_about_api_view,
        name="get-high-school-about-api-view",
    ),
    path(
        "high-school/<int:high_school_id>/faculty/<int:faculty_id>/remove/",
        remove_faculty_from_high_school_api_view,
        name="remove-faculty-from-high-school-api-view",
    ),
    path(
        "high-school-faculties/<int:high_school_id>/<str:mode>/",
        get_high_school_faculties_api_view,
        name="get-high-school-faculties",
    ),
    path(
        "create-high-school-faculties/",
        create_high_school_faculty_api_view,
        name="create-high-school-faculties-api-view",
    ),
    path("high-schools/", HighSchoolListAPIView.as_view(), name="high-school-list"),
    path(
        "high-schools/<int:id>/",
        HighSchoolRetrieveDestroyAPIView.as_view(),
        name="high-school-update-destroy",
    ),
    # Faculty routes
    path(
        "faculties-with-additional/",
        get_faculties_with_additional_data_api_view,
        name="get-faculties-with-additional-data",
    ),
    path(
        "faculties/",
        FacultyListCreateAPIView.as_view(),
        name="faculty-list-create",
    ),
    path(
        "faculties/<int:id>/",
        FacultyRetrieveUpdateDestroyAPIView.as_view(),
        name="faculty-retrieve-update-destroy",
    ),
    # Department routes
    path(
        "departments-with-additional/",
        get_departments_with_additional_data_api_view,
        name="get-departments-with-additional-data",
    ),
    path(
        "departments/",
        DepartmentListCreateAPIView.as_view(),
        name="department-list-create",
    ),
    path(
        "departments/<int:id>/",
        DepartmentRetrieveUpdateDestroyAPIView.as_view(),
        name="department-retrieve-update-destroy",
    ),
    # Degree routes
    path(
        "degrees/",
        DegreeListCreateAPIView.as_view(),
        name="degree-list-create",
    ),
    path(
        "degrees/<int:id>/",
        DegreeRetrieveUpdateDestroyAPIView.as_view(),
        name="degree-retrieve-update-destroy",
    ),
    # Classificator routes
    path(
        "classificators/",
        ClassificatorListCreateAPIView.as_view(),
        name="classificator-list-create",
    ),
    path(
        "classificators/<int:id>/",
        ClassificatorRetrieveUpdateDestroyAPIView.as_view(),
        name="classificator-retrieve-update-destroy",
    ),
    # Specialization routes
    path(
        "specializations/",
        SpecializationListCreateAPIView.as_view(),
        name="specialization-list-create",
    ),
    path(
        "specializations/<int:id>/",
        SpecializationRetrieveUpdateDestroyAPIView.as_view(),
        name="specialization-retrieve-update-destroy",
    ),
    # Student routes
    path(
        "students/",
        StudentListAPIView.as_view(),
        name="student-list-create",
    ),
    path(
        "students/<int:id>/",
        StudentRetrieveUpdateDestroyAPIView.as_view(),
        name="student-retrieve-update-destroy",
    ),
    # Nationality routes
    path(
        "nationalities/",
        NationalityListCreateAPIView.as_view(),
        name="nationality-list-create",
    ),
    path(
        "nationalities/<int:id>/",
        NationalityRetrieveUpdateDestroyAPIView.as_view(),
        name="nationality-retrieve-update-destroy",
    ),
    path("student-count-by-nationality/", get_students_count_by_nationality_all),
    path(
        "student-count-by-nationality/<int:nationality_id>/",
        get_students_count_by_nationality,
    ),
]
