import io

import openpyxl
from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponse
from django.utils import timezone
from rest_framework.decorators import api_view
from rest_framework.request import HttpRequest
from rest_framework.response import Response

from .decorators import validate_payload
from .models import (
    Degree,
    Department,
    Faculty,
    HighSchool,
    Nationality,
    Profile,
    Specialization,
)
from .serializers import DegreeSerializer, DepartmentSerializer, HighSchoolSerializer
from .utils import create_example


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


# Dashboard API view


@api_view(http_method_names=["GET"])
def root_dashboard_api_view(request: HttpRequest):
    if request.user.is_superuser:
        return Response(
            {
                "high_schools_count": HighSchool.objects.filter(active=True).count(),
                "faculties_count": Faculty.objects.filter(active=True).count(),
                "departments_count": Department.objects.filter(active=True).count(),
                "specializations_count": Specialization.objects.filter(
                    active=True
                ).count(),
                "nationalities_count": Nationality.objects.all().count(),
            }
        )
    else:
        return Response({"detail": "Permission denied."})


# High school API views


@api_view(http_method_names=["POST"])
@validate_payload(keys=["name", "abbreviation", "username", "password"])
def create_high_school_api_view(request: HttpRequest):
    user = User.objects.create_user(
        username=request.data["username"],
        email="stub@mail.com",
        password=request.data["password"],
    )
    profile = Profile.objects.get(user=user)
    profile.password = request.data["password"]
    profile.save()
    high_school = HighSchool.objects.create(
        name=request.data["name"],
        abbreviation=request.data["abbreviation"],
        manager=user,
    )
    return Response({"detail": "Success", "id": high_school.id})


@api_view(http_method_names=["GET"])
def get_high_schools_api_view(request: HttpRequest):
    high_school_serializer = HighSchoolSerializer(
        HighSchool.objects.filter(active=True), many=True
    )
    return Response(high_school_serializer.data)


@api_view(http_method_names=["GET"])
def get_high_school_api_view(request: HttpRequest, high_school_id: int):
    if HighSchool.objects.filter(id=high_school_id).exists():
        high_school = HighSchool.objects.get(id=high_school_id)
    else:
        return Response({"detail": "High school doesn't exist"})
    high_school_serializer = HighSchoolSerializer(high_school)
    return Response(high_school_serializer.data)


# Department API views


@api_view(http_method_names=["POST"])
@validate_payload(keys=["name", "abbreviation"])
def create_department_api_view(request: HttpRequest):
    department = Department.objects.create(
        name=request.data["name"],
        abbreviation=request.data["abbreviation"],
    )
    return Response({"detail": "Success", "id": department.id})


@api_view(http_method_names=["GET"])
def get_departments_api_view(request: HttpRequest):
    department_serializer = DepartmentSerializer(
        Department.objects.filter(active=True), many=True
    )
    return Response(department_serializer.data)


@api_view(http_method_names=["GET"])
def get_department_api_view(request: HttpRequest, department_id: int):
    if Department.objects.filter(id=department_id).exists():
        department = HighSchool.objects.get(id=department_id)
    else:
        return Response({"detail": "Department doesn't exist"})
    department_serializer = HighSchoolSerializer(department)
    return Response(department_serializer.data)


# Degree API views


@api_view(http_method_names=["POST"])
@validate_payload(keys=["name", "duration"])
def create_degree_api_view(request: HttpRequest):
    degree = Degree.objects.create(
        name=request.data["name"],
        duration=int(request.data["duration"]),
    )
    return Response({"detail": "Success", "id": degree.id})


@api_view(http_method_names=["GET"])
def get_degrees_api_view(request: HttpRequest):
    degree_serializer = DegreeSerializer(Degree.objects.filter(active=True), many=True)
    return Response(degree_serializer.data)


@api_view(http_method_names=["GET"])
def get_degree_api_view(request: HttpRequest, degree_id: int):
    if Degree.objects.filter(id=degree_id).exists():
        degree = HighSchool.objects.get(id=degree_id)
    else:
        return Response({"detail": "Degree doesn't exist"})
    degree_serializer = HighSchoolSerializer(degree)
    return Response(degree_serializer.data)


# Specialization API views
