from rest_framework.request import HttpRequest

from api.models import Profile

from .models import ActionLog


def is_admin(request: HttpRequest):
    return Profile.objects.get(user=request.user).role in ["superuser"]


def action_logger(request: HttpRequest, message: str):
    ActionLog.objects.create(user=request.user, action=message)
