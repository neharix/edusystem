from typing import List

from django.apps import apps
from rest_framework.request import HttpRequest

from .objects import Null

null = Null()


def is_valid_payload(request: HttpRequest, keys: List[str]):
    validation_list = [request.data.get(key, null) for key in keys]
    return not (null in validation_list)


def is_valid_files(request: HttpRequest, keys: List[str]):
    validation_list = [request.data.get(key, False) for key in keys]
    return not (False in validation_list)


def get_global_models():
    model_names: List[str] = []
    for model in apps.get_models():
        if (
            not model._meta.app_label == "admin"
            and not model._meta.app_label == "contenttypes"
            and not model._meta.app_label == "sessions"
        ) and (not model._meta.object_name == "Permission"):
            model_names.append(f"{model._meta.app_label}.{model._meta.object_name}")
    return model_names


def get_app_models(app_name: str):
    model_names: List[str] = []
    for model in apps.get_models():
        if (
            model._meta.object_name == "User"
            or model._meta.object_name == "Group"
            or model._meta.object_name == "Profile"
            or model._meta.app_label == app_name
        ):
            model_names.append(f"{model._meta.app_label}.{model._meta.object_name}")
    return model_names


def file_iterator(file_path, chunk_size=8192):
    with open(file_path, "rb") as file:
        while True:
            chunk = file.read(chunk_size)
            if not chunk:
                break
            yield chunk
