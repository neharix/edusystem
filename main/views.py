import os

from django.conf import settings
from django.http import FileResponse, Http404
from django.http import HttpRequest as DjangoRequest
from django.http import HttpResponseForbidden
from django.shortcuts import redirect, render
from django.utils import timezone
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


def clear_log_file(request: DjangoRequest):
    if request.user.is_superuser:
        log_path = os.path.join(settings.BASE_DIR, "requests.log")
        if os.path.exists(log_path):
            now = timezone.now().strftime("%d-%m-%Y-%H-%M-%S")
            response = FileResponse(
                open(log_path, "rb"),
                as_attachment=True,
                filename=f"requests-dump-{now}.log",
            )
            with open(log_path, "w") as logs_file:
                logs_file.write(f"--- CLEARED AT {now} ---")
            return response
        else:
            return Http404("Log file not found")
    else:
        return HttpResponseForbidden()
