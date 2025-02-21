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
        "high-school-departments/<int:high_school_id>/<str:mode>/",
        get_high_school_departments_api_view,
        name="get-high-school-departments",
    ),
    path(
        "high-school-specializations/<int:high_school_id>/<str:mode>/",
        get_high_school_specializations_api_view,
        name="get-high-school-departments",
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
        "remove/faculty-department/<int:faculty_department_id>/",
        remove_department_from_faculty_api_view,
        name="remove-department-from-faculty-api-view",
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
    path(
        "create-high-school-faculties/",
        create_high_school_faculty_api_view,
        name="create-high-school-faculties-api-view",
    ),
    # Department routes
    path(
        "departments-with-additional/",
        get_departments_with_additional_data_api_view,
        name="get-departments-with-additional-data",
    ),
    path(
        "remove/department-specialization/<int:department_specialization_id>/",
        remove_specialization_from_department_api_view,
        name="remove-specialization-from-department-api-view",
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
    path(
        "create-faculty-departments/",
        create_faculty_departments_api_view,
        name="create-faculty-departments-api-view",
    ),
    # Degree routes
    path(
        "degrees-with-additional/",
        get_degrees_with_additional_data_api_view,
        name="get-degrees-with-additional-data",
    ),
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
        "classificators-with-additional/",
        get_classificators_with_additional_data_api_view,
        name="get-classificators-with-additional-data",
    ),
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
        "specializations-with-additional/",
        get_specializations_with_additional_data_api_view,
        name="get-specializations-with-additional-data",
    ),
    path(
        "create-department-specializations/",
        create_department_specializations_api_view,
        name="create-department-specializations-api-view",
    ),
    path(
        "specializations/",
        SpecializationListCreateAPIView.as_view(),
        name="specialization-list-create",
    ),
    path(
        "update-specialization/<int:id>/",
        put_specialization_api_view,
        name="put-specialization-api-view",
    ),
    path(
        "specializations/<int:id>/",
        SpecializationRetrieveUpdateDestroyAPIView.as_view(),
        name="specialization-retrieve-update-destroy",
    ),
    # Student routes
    path("import-students/", import_students_from_excel_api_view),
    path(
        "students/",
        StudentListAPIView.as_view(),
        name="student-list",
    ),
    path(
        "students-info/<int:id>/",
        StudentInfoAPIView.as_view(),
        name="student-info",
    ),
    path(
        "students-with-additional/",
        get_students_with_additional_data_api_view,
        name="get-students-with-additional-data",
    ),
    path(
        "students/<int:id>/",
        StudentRetrieveUpdateDestroyAPIView.as_view(),
        name="student-retrieve-update-destroy",
    ),
    # Nationality routes
    path(
        "nationalizations-with-additional/",
        get_nationalizations_with_additional_data_api_view,
        name="get-nationalizations-with-additional-data",
    ),
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
    # Country routes
    path(
        "countries-with-additional/",
        get_countries_with_additional_data_api_view,
        name="get-countries-with-additional-data",
    ),
    path(
        "countries/",
        CountryListCreateAPIView.as_view(),
        name="country-list-create",
    ),
    path(
        "countries/<int:id>/",
        CountryRetrieveUpdateDestroyAPIView.as_view(),
        name="country-retrieve-update-destroy",
    ),
]
