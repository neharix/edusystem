import datetime
import io
import os
import subprocess
import sys
import zipfile

from django.conf import settings
from django.http import FileResponse, Http404
from django.http import HttpRequest
from django.http import HttpRequest as DjangoRequest
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import redirect, render
from django.utils import timezone
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import CustomTokenObtainPairSerializer
from .utils import get_global_models

os.environ["PGPASSWORD"] = settings.DATABASES["default"]["PASSWORD"]
os.environ["PYTHONUTF8"] = "1"

MODELS = get_global_models()


@permission_classes([IsAuthenticated])
@api_view(http_method_names=["GET", "POST", "PATCH", "DELETE", "PUT"])
def echo(request: HttpRequest):
    return Response({"detail": "The API works correctly"})


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
            outputs = []
            env = os.environ.copy()
            env["PYTHONUTF8"] = "1"
            for model in MODELS:
                outputs.append(
                    subprocess.check_output(
                        [
                            sys.executable,
                            "manage.py",
                            "dumpdata",
                            model,
                            "--natural-foreign",
                            "--natural-primary",
                            "--indent",
                            "2",
                        ],
                        stderr=subprocess.STDOUT,
                        text=True,
                        encoding="utf-8",
                        env=env,
                    )
                    .encode("utf-8", "ignore")
                    .decode("utf-8")
                )

            buffer = io.BytesIO()

            with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
                for i, data in enumerate(outputs):
                    filename = f"{MODELS[i].replace('.', '_').lower()}.json"
                    zip_file.writestr(filename, data)

            buffer.seek(0)

            response = HttpResponse(buffer.read(), content_type="application/zip")
            response["Content-Disposition"] = (
                f'attachment; filename="bmdu-dump-{datetime.datetime.now().strftime('%d-%m-%Y-%H%M%S')}.zip"'
            )

            return response

        except subprocess.CalledProcessError as e:
            return HttpResponse(f"Ошибка выполнения: {e.output}", status=500)
    return HttpResponse("Знакомы?)", status=403)


def dump_sql_data_view(request: HttpRequest):
    if request.user.is_superuser:
        try:
            now = datetime.datetime.now().strftime("%d-%m-%Y-%H%M%S")
            subprocess.run(
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
            )
            with open(
                os.path.join(settings.BASE_DIR / f"data-{now}.sql"), "r"
            ) as sql_file:
                attachment = sql_file.read()

            os.remove(os.path.join(settings.BASE_DIR / f"data-{now}.sql"))

            response = HttpResponse(
                attachment, content_type="application/plain; charset=utf-8"
            )
            response["Content-Disposition"] = f"attachment; filename=data-{now}.sql"
            return response
        except subprocess.CalledProcessError as e:
            return HttpResponse(f"Ошибка выполнения: {e.output}", status=500)
        # except Exception as e:
        # return HttpResponse(f"Ошибка выполнения: {e}", status=500)
    return HttpResponse("Знакомы?)", status=403)
