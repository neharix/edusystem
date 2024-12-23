import io

import openpyxl
from django.http import HttpRequest, HttpResponse
from django.utils import timezone
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.request import HttpRequest
from rest_framework.response import Response

from .models import *
from .utils import create_example


# @permission_classes((IsAuthenticated))
@api_view(http_method_names=["POST"])
def check_data(request: HttpRequest):
    workbook = openpyxl.load_workbook(request.FILES.get("file"))
    worksheet = workbook["maglumat"]
    print(worksheet["H2"].value)
    workbook.close()

    return Response({"detail": "hello"})


@api_view(http_method_names=["GET"])
def get_example(request: HttpRequest, high_school_id: int, row_count: int):
    if HighSchool.objects.filter(id=high_school_id).exists():
        high_school = HighSchool.objects.get(id=high_school_id)
    else:
        return HttpResponse({"detail": "High school isn't found"})

    workbook = create_example(row_count, high_school)

    with io.BytesIO() as buffer:
        workbook.save(buffer)
        content = buffer.getvalue()

    response = HttpResponse(
        content=content,
        content_type="application/xlsx",
    )
    response["Content-Disposition"] = f'attachment; filename="form.xlsx"'
    return response
