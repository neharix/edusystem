"""
URL configuration for server project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

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
    path("create-department/", create_department_api_view),
    path("departments/", get_departments_api_view),
    path("department/<int:department_id>/", get_department_api_view),
    # Degree routes
    path("create-degree/", create_department_api_view),
    path("degrees/", get_degrees_api_view),
    path("degree/<int:degree_id>/", get_degree_api_view),
    # Classificator routes
    path("create-classificator/", create_classificator_api_view),
    path("classificators/", get_classificators_api_view),
    path("classificator/<int:classificator_id>/", get_classificator_api_view),
]
