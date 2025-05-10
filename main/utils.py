from typing import List

from django.apps import apps


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
