import datetime
import io
import os
import subprocess
import sys

from django.conf import settings
from django.http import FileResponse, Http404
from django.http import HttpRequest
from django.http import HttpRequest as DjangoRequest
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import redirect, render
from django.utils import timezone
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import CustomTokenObtainPairSerializer

os.environ["PGPASSWORD"] = settings.DATABASES["default"]["PASSWORD"]
os.environ["PYTHONUTF8"] = "1"


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
            with open(log_path, "rb") as logs_file:
                buffer = io.BytesIO(logs_file.read())
            response = FileResponse(
                buffer,
                as_attachment=True,
                filename=f"requests-dump-{now}.log",
            )
            with open(log_path, "w") as logs_file:
                logs_file.write(f"--- CLEARED AT {now} ---\n")
            return response
        else:
            return Http404("Log file not found")
    else:
        return HttpResponseForbidden()


def dump_json_data_view(request: HttpRequest):
    if request.user.is_superuser:
        try:
            env = os.environ.copy()
            env["PYTHONUTF8"] = "1"
            output = subprocess.check_output(
                [
                    sys.executable,
                    "manage.py",
                    "dumpdata",
                    "--natural-foreign",
                    "--natural-primary",
                    "-e",
                    "contenttypes",
                    "--exclude",
                    "admin.logentry",
                    "--exclude",
                    "auth.permission",
                    "--indent",
                    "2",
                ],
                stderr=subprocess.STDOUT,
                text=True,
                encoding="utf-8",
                env=env,
            )

            output = output.encode("utf-8", "ignore").decode("utf-8")

            response = HttpResponse(
                output, content_type="application/json; charset=utf-8"
            )
            response["Content-Disposition"] = "attachment; filename=dumpdata.json"
            return response

        except subprocess.CalledProcessError as e:
            return HttpResponse(f"Ошибка выполнения: {e.output}", status=500)
    return HttpResponse("Знакомы?)", status=403)


def dump_sql_data_view(request: HttpRequest):
    if request.user.is_superuser:
        try:
            env = os.environ.copy()
            now = datetime.datetime.now().strftime("%d-%m-%Y-%H%M%S")
            output = subprocess.check_output(
                [
                    "pg_dump",
                    "-f",
                    f"data-{now}.sql",
                    "-h",
                    settings.DATABASES["default"]["HOST"],
                    "-U",
                    settings.DATABASES["default"]["USER"],
                    "-d",
                    settings.DATABASES["default"]["NAME"],
                    "-p",
                    settings.DATABASES["default"]["PORT"],
                ],
                stderr=subprocess.STDOUT,
                text=True,
                encoding="utf-8",
                env=env,
            )
            output = output.encode("utf-8", "ignore").decode("utf-8")

            response = HttpResponse(
                output, content_type="application/plain; charset=utf-8"
            )
            response["Content-Disposition"] = f"attachment; filename=data-{now}.sql"
            return response
        except subprocess.CalledProcessError as e:
            return HttpResponse(f"Ошибка выполнения: {e.output}", status=500)
        # except Exception as e:
        # return HttpResponse(f"Ошибка выполнения: {e}", status=500)
    return HttpResponse("Знакомы?)", status=403)
