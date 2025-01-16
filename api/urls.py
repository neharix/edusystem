from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import *

urlpatterns = [
    # Authentication routes
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # Special routes
    path(
        "get-example/high-school/<int:high_school_id>/row-count/<int:row_count>/",
        get_example,
    ),
    path("import-excel-data/", import_excel_data),
    path("root-dashboard/", root_dashboard_api_view),
    # High school routes
    path("create-high-school/", create_high_school_api_view),
    path("high-schools/", get_high_schools_api_view),
    path("high-school/<int:high_school_id>/", get_high_school_api_view),
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
    path("create-classificator/", create_classificator_api_view),
    path("classificators/", get_classificators_api_view),
    path("classificator/<int:classificator_id>/", get_classificator_api_view),
    # Specialization routes
    path("create-specialization/", create_specialization_api_view),
    path("specializations/", get_specializations_api_view),
    path("specialization/<int:specialization_id>/", get_specialization_api_view),
    # Student routes
    path("students/", get_students_api_view),
    path("student/<int:student_id>/", get_student_api_view),
]
