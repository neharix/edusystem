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
    path(
        "get-example/high-school/<int:high_school_id>/row-count/<int:row_count>/",
        get_example,
    ),
    path("import-excel-data/", import_excel_data),
    path("root-dashboard/", root_dashboard_api_view),
    # High school routes
    path("create-high-school/", create_high_school_api_view),
    path("high-schools/", HighSchoolListAPIView.as_view(), name="high-school-list"),
    path(
        "high-schools/<int:id>/",
        HighSchoolRetrieveUpdateDestroyAPIView.as_view(),
        name="high-school-retrieve-update-destroy",
    ),
    # Department routes
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
