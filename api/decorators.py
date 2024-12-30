from functools import wraps
from typing import Dict, List

from django.shortcuts import redirect
from rest_framework.request import HttpRequest
from rest_framework.response import Response


def validate_post(keys: List[str]):
    def method_wrapper(view):
        def args_wrapper(request: HttpRequest, *args, **kwargs):
            validation_list = [request.data.get(key, False) for key in keys]
            if False in validation_list:
                return Response({"detail": "Payload invalid"})
            else:
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
