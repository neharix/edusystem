import os

from django.conf import settings
from django.http import FileResponse, Http404
from django.http import HttpRequest as DjangoRequest
from django.http import HttpResponseForbidden
from django.shortcuts import redirect, render
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import CustomTokenObtainPairSerializer


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


def dev_tools(request: DjangoRequest):
    if request.user.is_superuser:
        return render(request, "main/dev_tools.html")
    elif request.user.is_authenticated:
        return HttpResponseForbidden()
    else:
        return redirect("/api/admin/login/")


def download_log_file(request: DjangoRequest):
    if request.user.is_superuser:
        log_path = os.path.join(settings.BASE_DIR, "requests.log")
        if os.path.exists(log_path):
            return FileResponse(
                open(log_path, "rb"), as_attachment=True, filename="requests.log"
            )
        else:
            return Http404("Log file not found")
    else:
        return HttpResponseForbidden()
