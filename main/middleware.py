import logging

from django.conf import settings
from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger("django.request")


class RequestLoggerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        logger.info(
            f"Method: {request.method} | Path: {request.path} | IP: {self.get_client_ip(request)} | Headers: {dict(request.headers)}\n"
        )
        # if request.method == "POST":
        #     logger.info(f"Request Body: {request.body.decode('utf-8')}")
        response = self.get_response(request)

        logger.info(f"Response Status: {response.status_code} | Path: {request.path}")
        return response

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")
        return ip


class DrfTitleMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        if isinstance(response, HttpResponse):
            postfix = getattr(settings, "REST_TITLE", "BMDU API")
            if (
                hasattr(response, "content")
                and b"django-rest-framework" in response.content
            ):
                response.content = response.content.replace(
                    b"Django REST framework", f"{postfix}".encode("utf-8")
                )
        return response
