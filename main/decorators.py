from typing import List

from rest_framework.request import HttpRequest
from rest_framework.response import Response

from .objects import Null

null = Null()


def login_required(is_admin: bool = False):
    def method_wrapper(view):
        def args_wrapper(request: HttpRequest, *args, **kwargs):
            if request.user.is_anonymous:
                return Response({"detail": "Unauthorized"}, status=401)

            if not request.user.is_superuser and is_admin:
                return Response({"detail": "Permission denied"}, status=403)
            return view(request, *args, **kwargs)

        return args_wrapper

    return method_wrapper


def validate_payload(keys: List[str]):
    def method_wrapper(view):
        def args_wrapper(request: HttpRequest, *args, **kwargs):
            if request.method in ["POST", "PUT", "PATCH"]:
                validation_list = [request.data.get(key, null) for key in keys]
                if null in validation_list:
                    print("Payload invalid", request.data)
                    return Response({"detail": "Payload invalid"}, status=400)
            return view(request, *args, **kwargs)

        return args_wrapper

    return method_wrapper


def validate_files(keys: List[str]):
    def method_wrapper(view):
        def args_wrapper(request: HttpRequest, *args, **kwargs):
            validation_list = [request.data.get(key, False) for key in keys]
            if False in validation_list:
                return Response({"detail": "Files dictionary invalid"})
            else:
                return view(request, *args, **kwargs)

        return args_wrapper

    return method_wrapper
