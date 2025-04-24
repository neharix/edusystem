import json
import os

from django.conf import settings
from rest_framework.request import HttpRequest
from rest_framework.response import Response

from api.models import Profile


def login_required(is_admin: bool = False):
    def method_wrapper(view):
        def args_wrapper(request: HttpRequest, *args, **kwargs):
            if request.user.is_anonymous:
                return Response({"detail": "Unauthorized"}, status=401)

            if (
                Profile.objects.get(user=request.user).role not in ["superuser"]
                and is_admin
            ):
                return Response({"detail": "Permission denied"}, status=403)
            return view(request, *args, **kwargs)

        return args_wrapper

    return method_wrapper


def check_service_status():
    def method_wrapper(view):
        def args_wrapper(request: HttpRequest, *args, **kwargs):
            with open(
                os.path.join(settings.BASE_DIR / "conf/mmu.json"), "r", encoding="utf-8"
            ) as cfg_file:
                is_enabled = json.loads(cfg_file.read())["is_enabled"]
            if not is_enabled and not request.user.is_superuser:
                return Response({"detail": "Service Unavailable"}, status=503)
            return view(request, *args, **kwargs)

        return args_wrapper

    return method_wrapper
