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
    path("try-otp/<str:username>/", try_otp_api_view, name="otp"),
    # Special routes
    path("dashboard/", dashboard_api_view),
]
