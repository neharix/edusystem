from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import *

urlpatterns = [
    # path("/", view, name=""),
    # Authentication routes
    path("token/", TokenObtainPairView.as_view(), name="token-obtain-pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
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
    path("export/", export_data),
    path("import/", import_data),
    # Profile routes
    path("profiles/", profile_list_view, name="profile-list"),
]
