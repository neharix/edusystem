import datetime
import io
import subprocess

import numpy as np
import pandas as pd
import pytz
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.http import HttpRequest as DjangoHttpRequest
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.utils import timezone
from django.utils.text import slugify
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import (
    DestroyAPIView,
    ListAPIView,
    ListCreateAPIView,
    RetrieveAPIView,
    RetrieveDestroyAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import IsAdminUser
from rest_framework.request import HttpRequest
from rest_framework.response import Response

from .decorators import validate_files, validate_payload
from .models import (
    AnnualUpdateReport,
    Classificator,
    Country,
    Degree,
    Department,
    DepartmentSpecialization,
    DiplomaReport,
    DiplomaRequest,
    DiplomaRequestAction,
    ExpulsionReason,
    ExpulsionRequest,
    Faculty,
    FacultyDepartment,
    HighSchool,
    HighSchoolFaculty,
    Nationality,
    Profile,
    Region,
    ReinstateRequest,
    Specialization,
    Student,
    TeacherStatement,
)
from .serializers import (
    ClassificatorSerializer,
    CountrySerializer,
    DegreeSerializer,
    DepartmentSerializer,
    DiplomaRequestSerializer,
    ExpelledStudentInfoSerializer,
    ExpulsionReasonSerializer,
    ExpulsionRequestSerializer,
    FacultySerializer,
    GraduateAdditionalSerializer,
    GraduateInfoSerializer,
    HighSchoolSerializer,
    NationalitySerializer,
    ProfileSerializer,
    RegionSerializer,
    ReinstateRequestSerializer,
    SpecializationSerializer,
    StudentAdditionalSerializer,
    StudentInfoSerializer,
    StudentSerializer,
    TeacherStatementSerializer,
    advanced_diploma_serializer,
)
from .utils import (
    advanced_filter,
    advanced_quantity_filter,
    create_example,
    filter_by_query,
    validate_not_null_field,
)

ADMISSION_START_RANGE = 2017

# Dumper view

import os
import subprocess
import sys

from django.http import HttpResponse


@api_view(http_method_names=["GET"])
def dumpdata_view(request: HttpRequest):
    if request.user.is_superuser:
        try:
            env = os.environ.copy()
            env["PYTHONUTF8"] = "1"
            output = subprocess.check_output(
                [
                    sys.executable,
                    "manage.py",
                    "dumpdata",
                    "--exclude",
                    "admin.logentry",
                    "--exclude",
                    "auth.permission",
                    "--indent",
                    "2",
                ],
                stderr=subprocess.STDOUT,
                text=True,
                encoding="utf-8",
                env=env,
            )

            output = output.encode("utf-8", "ignore").decode(
                "utf-8"
            )  # Убираем битые символы

            response = HttpResponse(
                output, content_type="application/json; charset=utf-8"
            )
            response["Content-Disposition"] = "attachment; filename=dumpdata.json"
            return response

        except subprocess.CalledProcessError as e:
            return HttpResponse(f"Ошибка выполнения: {e.output}", status=500)
    return HttpResponse("Знакомы?)", status=403)


# Login/logout view


# def login_view(request: DjangoHttpRequest):
#     if request.user.is_anonymous:
#         if request.method == "POST":
#             form = AuthenticationForm(request, data=request.POST)
#             if form.is_valid():
#                 user = form.get_user()
#                 login(request, user)
#                 return redirect("redoc")
#         form = AuthenticationForm()

#         return render(request, "api/login.html", {"form": form})
#     else:
#         return redirect("redoc")


def logout_view(request: DjangoHttpRequest):
    logout(request)
    return redirect("/api/v1/admin/login/")


# Special API views


@api_view(http_method_names=["GET"])
def update_study_years_api_view(request: HttpRequest):
    if request.user.is_superuser:
        if not AnnualUpdateReport.objects.filter(updated_at__year=timezone.now().year):
            students = Student.objects.filter(is_obsolete=False, is_expelled=False)
            default_students = students.exclude(study_year__contains="DÖB")
            for student in default_students:
                if student.study_year.isdigit():
                    if student.specialization.specialization.degree.duration == int(
                        student.study_year
                    ):
                        student.is_obsolete = True
                    else:
                        student.study_year = int(student.study_year) + 1
                student.save()

            # Обновление курса бакалавров с языковым обучением
            students.filter(study_year__contains="DÖB").update(study_year="1")
            AnnualUpdateReport.objects.create()

            return Response({"is_successfully": True})
        return Response({"is_successfully": False}, status=406)
    else:
        return Response({"is_successfully": False}, status=403)


class ProfileRetrieveApiView(RetrieveAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    lookup_field = "id"


@api_view(http_method_names=["GET", "POST", "PATCH", "DELETE", "PUT"])
def echo(request: HttpRequest):
    return Response({"detail": "The API works correctly"})


@api_view(http_method_names=["GET"])
def get_user_data(request: HttpRequest):
    if request.user.is_superuser:
        notifications = []
        for expulsion_request in ExpulsionRequest.objects.filter(
            is_obsolete=False, verdict=None
        ):
            if not request.user in expulsion_request.viewed_by.all():
                notifications.append(
                    {
                        "id": expulsion_request.id,
                        "sender": HighSchool.objects.get(
                            manager__user=expulsion_request.sender
                        ).abbreviation,
                        "type": "expulsion",
                    }
                )
        for reinstate_request in ReinstateRequest.objects.filter(
            is_obsolete=False, verdict=None
        ):
            if not request.user in reinstate_request.viewed_by.all():
                notifications.append(
                    {
                        "id": reinstate_request.id,
                        "sender": HighSchool.objects.get(
                            manager__user=reinstate_request.sender
                        ).abbreviation,
                        "type": "reinstate",
                    }
                )
        for teacher_statement in TeacherStatement.objects.filter(
            is_obsolete=False, verdict=None
        ):
            if not request.user in teacher_statement.viewed_by.all():
                notifications.append(
                    {
                        "id": teacher_statement.id,
                        "sender": HighSchool.objects.get(
                            manager__user=teacher_statement.sender
                        ).abbreviation,
                        "type": "teacher",
                    }
                )

        for diploma_request in DiplomaRequest.objects.filter(is_obsolete=False):
            if not request.user in diploma_request.viewed_by.all():
                notifications.append(
                    {
                        "id": diploma_request.id,
                        "sender": HighSchool.objects.get(
                            manager__user=diploma_request.sender
                        ).abbreviation,
                        "type": "diploma",
                    }
                )
        return Response(
            {
                "id": request.user.id,
                "email": request.user.email,
                "is_superuser": request.user.is_superuser,
                "notifications": notifications,
            }
        )
    else:
        return Response(
            {
                "id": request.user.id,
                "manager_of": HighSchool.objects.get(
                    manager__user=request.user
                ).abbreviation,
                "email": request.user.email,
                "is_superuser": request.user.is_superuser,
            }
        )


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
    filename = slugify(high_school.abbreviation + " üçin forma") + ".xlsx"
    response["Content-Disposition"] = f'attachment; filename="' + filename + '"'
    return response


@api_view(http_method_names=["GET"])
def dashboard_api_view(request: HttpRequest):
    if request.user.is_superuser:
        male_graduates = 0
        female_graduates = 0
        for specialization in Specialization.objects.filter(active=True):
            for d_specialization in DepartmentSpecialization.objects.filter(
                specialization=specialization
            ):
                male_graduates += Student.objects.filter(
                    specialization=d_specialization,
                    study_year=str(specialization.degree.duration),
                    gender="M",
                    active=True,
                    is_expelled=False,
                    is_obsolete=False,
                ).count()
                female_graduates += Student.objects.filter(
                    specialization=d_specialization,
                    study_year=str(specialization.degree.duration),
                    gender="F",
                    active=True,
                    is_expelled=False,
                    is_obsolete=False,
                ).count()

        return Response(
            {
                "high_schools_count": HighSchool.objects.filter(active=True).count(),
                "faculties_count": Faculty.objects.filter(active=True).count(),
                "departments_count": Department.objects.filter(active=True).count(),
                "specializations_count": Specialization.objects.filter(
                    active=True
                ).count(),
                "nationalities_count": Nationality.objects.all().count(),
                "students_count": Student.objects.filter(
                    active=True, is_expelled=False
                ).count(),
                "male_students_count": Student.objects.filter(
                    gender="M", active=True, is_expelled=False, is_obsolete=False
                ).count(),
                "female_students_count": Student.objects.filter(
                    gender="F", active=True, is_expelled=False, is_obsolete=False
                ).count(),
                "male_graduates": male_graduates,
                "female_graduates": female_graduates,
                "admissions": [
                    {
                        "year": year,
                        "male_students_count": Student.objects.filter(
                            gender="M",
                            admission_date__year=year,
                            active=True,
                            is_expelled=False,
                            is_obsolete=False,
                        ).count(),
                        "female_students_count": Student.objects.filter(
                            gender="F",
                            admission_date__year=year,
                            active=True,
                            is_expelled=False,
                            is_obsolete=False,
                        ).count(),
                    }
                    for year in range(ADMISSION_START_RANGE, timezone.now().year + 1)
                ],
            }
        )
    elif request.user.is_authenticated:
        high_school = HighSchool.objects.get(manager__user=request.user)
        return Response(
            {
                "faculties_count": HighSchoolFaculty.objects.filter(
                    high_school=high_school
                ).count(),
                "departments_count": FacultyDepartment.objects.filter(
                    high_school_faculty__high_school=high_school
                ).count(),
                "specializations_count": DepartmentSpecialization.objects.filter(
                    faculty_department__high_school_faculty__high_school=high_school
                ).count(),
                # FIXME
                "nationalities_count": Nationality.objects.all().count(),
                "students_count": Student.objects.filter(
                    active=True,
                    high_school=high_school,
                    is_expelled=False,
                    is_obsolete=False,
                ).count(),
                "male_students_count": Student.objects.filter(
                    gender="M",
                    high_school=high_school,
                    active=True,
                    is_expelled=False,
                    is_obsolete=False,
                ).count(),
                "female_students_count": Student.objects.filter(
                    gender="F",
                    high_school=high_school,
                    active=True,
                    is_expelled=False,
                    is_obsolete=False,
                ).count(),
                "admissions": [
                    {
                        "year": year,
                        "male_students_count": Student.objects.filter(
                            high_school=high_school,
                            gender="M",
                            admission_date__year=year,
                            active=True,
                        ).count(),
                        "female_students_count": Student.objects.filter(
                            high_school=high_school,
                            gender="F",
                            admission_date__year=year,
                            active=True,
                        ).count(),
                    }
                    for year in range(ADMISSION_START_RANGE, timezone.now().year + 1)
                ],
            }
        )
    return Response({"detail": "Permission denied."})


# High school API views


@api_view(http_method_names=["POST"])
@validate_payload(keys=["high_school_name", "abbreviation", "username", "password"])
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
        name=request.data["high_school_name"],
        abbreviation=request.data["abbreviation"],
        manager=profile,
        active=True,
    )
    return Response({"detail": "Success", "id": high_school.id})


@api_view(http_method_names=["PUT"])
@validate_payload(keys=["high_school_name", "abbreviation", "username", "password"])
def put_high_school_api_view(request: HttpRequest, high_school_id: int):
    if HighSchool.objects.filter(id=high_school_id).exists():
        high_school = HighSchool.objects.get(id=high_school_id)
    else:
        return Response({"detail": "High school doesn't exist"}, status=404)

    high_school.name = request.data["high_school_name"]
    high_school.abbreviation = request.data["abbreviation"]
    high_school.save()

    user = high_school.manager.user
    profile = high_school.manager

    user.username = request.data["username"]
    user.set_password(request.data["password"])
    user.save()

    profile.password = request.data["password"]
    profile.save()
    return Response({"detail": "Success", "id": high_school.id})


@api_view(http_method_names=["GET"])
def get_high_school_with_additional_data_api_view(request: HttpRequest):
    if request.user.is_superuser:
        high_schools = HighSchool.objects.filter(active=True)
        response = []
        for high_school in high_schools:
            male_count = Student.objects.filter(
                high_school=high_school,
                gender="M",
                is_expelled=False,
                is_obsolete=False,
            ).count()
            female_count = Student.objects.filter(
                high_school=high_school,
                gender="F",
                is_expelled=False,
                is_obsolete=False,
            ).count()
            response.append(
                {
                    "id": high_school.id,
                    "name": high_school.name,
                    "students_count": male_count + female_count,
                    "male_count": male_count,
                    "female_count": female_count,
                }
            )
        return Response(response)
    return Response({"detail": "Permission denied"}, status=403)


@api_view(http_method_names=["GET"])
def get_high_school_about_api_view(request: HttpRequest, high_school_id: int):
    if HighSchool.objects.filter(id=high_school_id).exists():
        high_school = HighSchool.objects.get(id=high_school_id)
    else:
        return Response({"detail": "High school doesn't exist"}, status=404)
    return Response(
        {
            "students_count": Student.objects.filter(
                active=True, high_school=high_school
            ).count(),
            "male_students_count": Student.objects.filter(
                gender="M", high_school=high_school, active=True
            ).count(),
            "female_students_count": Student.objects.filter(
                gender="F", high_school=high_school, active=True
            ).count(),
            "admissions": [
                {
                    "year": year,
                    "male_students_count": Student.objects.filter(
                        high_school=high_school,
                        gender="M",
                        admission_date__year=year,
                        active=True,
                    ).count(),
                    "female_students_count": Student.objects.filter(
                        high_school=high_school,
                        gender="F",
                        admission_date__year=year,
                        active=True,
                    ).count(),
                }
                for year in range(ADMISSION_START_RANGE, timezone.now().year + 1)
            ],
            "students_count_by_regions": [
                {
                    "region": region.name,
                    "students_count": Student.objects.filter(
                        high_school=high_school,
                        region=region,
                        active=True,
                    ).count(),
                }
                for region in Region.objects.all()
            ],
        }
    )


@api_view(http_method_names=["GET"])
def get_high_school_faculties_api_view(
    request: HttpRequest, high_school_id: int, mode: str
):
    if not mode in ["exc", "inc"]:
        return Response({"detail": "Invalid mode"}, status=400)
    if HighSchool.objects.filter(id=high_school_id).exists():
        high_school = HighSchool.objects.get(id=high_school_id)
    else:
        return Response({"detail": "High school doesn't exist"}, status=404)
    high_school_faculty_identificators = [
        high_school_faculty.faculty.id
        for high_school_faculty in HighSchoolFaculty.objects.filter(
            high_school=high_school
        )
    ]
    if mode == "inc":
        return Response(
            FacultySerializer(
                Faculty.objects.filter(id__in=high_school_faculty_identificators),
                many=True,
            ).data
        )
    elif mode == "exc":
        return Response(
            FacultySerializer(
                Faculty.objects.exclude(
                    id__in=high_school_faculty_identificators
                ).filter(active=True),
                many=True,
            ).data
        )


@api_view(http_method_names=["GET"])
def get_high_school_departments_api_view(
    request: HttpRequest, high_school_id: int, mode: str
):
    if not mode in ["exc", "inc"]:
        return Response({"detail": "Invalid mode"}, status=400)
    if HighSchool.objects.filter(id=high_school_id).exists():
        high_school = HighSchool.objects.get(id=high_school_id)
    else:
        return Response({"detail": "High school doesn't exist"}, status=404)

    if mode == "inc":
        return Response(
            [
                {
                    "instance_id": faculty_department.id,
                    "id": faculty_department.department.id,
                    "name": faculty_department.department.name,
                    "abbreviation": faculty_department.department.abbreviation,
                    "active": faculty_department.department.active,
                    "faculty": faculty_department.high_school_faculty.faculty.name,
                }
                for faculty_department in FacultyDepartment.objects.filter(
                    high_school_faculty__high_school=high_school
                )
            ]
        )

    elif mode == "exc":
        high_school_department_identificators = [
            faculty_department.department.id
            for faculty_department in FacultyDepartment.objects.filter(
                high_school_faculty__high_school=high_school
            )
        ]
        return Response(
            DepartmentSerializer(
                Department.objects.exclude(
                    id__in=high_school_department_identificators
                ).filter(active=True),
                many=True,
            ).data
        )


@api_view(http_method_names=["GET"])
def get_high_school_specializations_api_view(
    request: HttpRequest, high_school_id: int, mode: str
):
    if not mode in ["exc", "inc"]:
        return Response({"detail": "Invalid mode"}, status=400)
    if HighSchool.objects.filter(id=high_school_id).exists():
        high_school = HighSchool.objects.get(id=high_school_id)
    else:
        return Response({"detail": "High school doesn't exist"}, status=404)

    if mode == "inc":
        return Response(
            [
                {
                    "instance_id": department_specialization.id,
                    "id": department_specialization.specialization.id,
                    "name": department_specialization.specialization.name,
                    "abbreviation": department_specialization.specialization.abbreviation,
                    "classificator": (
                        department_specialization.specialization.classificator.name
                        if department_specialization.specialization.classificator
                        else "Ýok"
                    ),
                    "active": department_specialization.specialization.active,
                    "department": department_specialization.faculty_department.department.name,
                }
                for department_specialization in DepartmentSpecialization.objects.filter(
                    faculty_department__high_school_faculty__high_school=high_school
                )
            ]
        )

    elif mode == "exc":
        high_school_specialization_identificators = [
            department_specialization.specialization.id
            for department_specialization in DepartmentSpecialization.objects.filter(
                faculty_department__high_school_faculty__high_school=high_school
            )
        ]
        return Response(
            SpecializationSerializer(
                Specialization.objects.exclude(
                    id__in=high_school_specialization_identificators
                ).filter(active=True),
                many=True,
            ).data
        )


@api_view(http_method_names=["GET"])
def remove_faculty_from_high_school_api_view(
    request: HttpRequest, high_school_id: int, faculty_id: int
):
    if HighSchool.objects.filter(id=high_school_id).exists():
        high_school = HighSchool.objects.get(id=high_school_id)
    else:
        return Response({"detail": "High school doesn't exist"}, status=404)
    if Faculty.objects.filter(id=faculty_id).exists():
        faculty = Faculty.objects.get(id=faculty_id)
    else:
        return Response({"detail": "Faculty doesn't exist"}, status=404)
    HighSchoolFaculty.objects.get(high_school=high_school, faculty=faculty).delete()
    return Response({"detail": "Success"})


class HighSchoolListAPIView(ListAPIView):
    queryset = HighSchool.objects.all()
    serializer_class = HighSchoolSerializer


class HighSchoolRetrieveDestroyAPIView(RetrieveDestroyAPIView):
    queryset = HighSchool.objects.all()
    serializer_class = HighSchoolSerializer
    lookup_field = "id"

    def delete(self, request: HttpRequest, id: int):
        instance = self.get_object()
        instance.active = False
        instance.save()
        return Response({"detail": "Success"})


# Faculty API views


@api_view(http_method_names=["GET"])
def get_faculties_with_additional_data_api_view(request: HttpRequest):
    response = []
    if request.user.is_superuser:
        faculties = Faculty.objects.filter(active=True)
        for faculty in faculties:
            male_count, female_count = 0, 0
            for h_faculty in HighSchoolFaculty.objects.filter(faculty=faculty):
                male_count += Student.objects.filter(
                    specialization__faculty_department__high_school_faculty=h_faculty,
                    gender="M",
                    is_expelled=False,
                    is_obsolete=False,
                ).count()
                female_count += Student.objects.filter(
                    specialization__faculty_department__high_school_faculty=h_faculty,
                    gender="F",
                    is_expelled=False,
                    is_obsolete=False,
                ).count()
            response.append(
                {
                    "id": faculty.id,
                    "name": faculty.name,
                    "students_count": male_count + female_count,
                    "male_count": male_count,
                    "female_count": female_count,
                }
            )
        return Response(response)
    else:
        high_school = HighSchool.objects.get(manager__user=request.user)
        faculties = [
            faculty.faculty
            for faculty in HighSchoolFaculty.objects.filter(high_school=high_school)
        ]
        for faculty in faculties:
            male_count, female_count = 0, 0
            for h_faculty in HighSchoolFaculty.objects.filter(
                high_school=high_school, faculty=faculty
            ):
                male_count += Student.objects.filter(
                    specialization__faculty_department__high_school_faculty=h_faculty,
                    gender="M",
                    is_expelled=False,
                    is_obsolete=False,
                ).count()
                female_count += Student.objects.filter(
                    specialization__faculty_department__high_school_faculty=h_faculty,
                    gender="F",
                    is_expelled=False,
                    is_obsolete=False,
                ).count()
            response.append(
                {
                    "id": faculty.id,
                    "name": faculty.name,
                    "students_count": male_count + female_count,
                    "male_count": male_count,
                    "female_count": female_count,
                    "departments_count": FacultyDepartment.objects.filter(
                        high_school_faculty__faculty=faculty,
                        high_school_faculty__high_school=high_school,
                    ).count(),
                }
            )
        return Response(response)


@api_view(http_method_names=["POST"])
@validate_payload(keys=["high_school", "faculties"])
def create_high_school_faculty_api_view(request: HttpRequest):
    if HighSchool.objects.filter(id=request.data["high_school"]).exists():
        high_school = HighSchool.objects.get(id=request.data["high_school"])
    else:
        return Response({"detail": "High school doesn't exist"}, status=404)

    for faculty_id in request.data["faculties"]:
        if Faculty.objects.filter(id=faculty_id).exists():
            faculty = Faculty.objects.get(id=faculty_id)
            if not HighSchoolFaculty.objects.filter(
                high_school=high_school, faculty=faculty
            ).exists():
                HighSchoolFaculty.objects.create(
                    high_school=high_school, faculty=faculty
                )
    return Response({"detail": "Success"})


@api_view(http_method_names=["GET"])
def remove_department_from_faculty_api_view(
    request: HttpRequest, faculty_department_id: int
):
    if FacultyDepartment.objects.filter(id=faculty_department_id).exists():
        FacultyDepartment.objects.get(id=faculty_department_id).delete()
    else:
        return Response({"detail": "Faculty department doesn't exist"}, status=404)
    return Response({"detail": "Success"})


class FacultyListCreateAPIView(ListCreateAPIView):
    queryset = Faculty.objects.all()
    serializer_class = FacultySerializer
    lookup_field = "id"


class FacultyRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Faculty.objects.all()
    serializer_class = FacultySerializer
    lookup_field = "id"

    def delete(self, request: HttpRequest, id: int):
        instance = self.get_object()
        instance.active = False
        instance.save()
        return Response({"detail": "Success"})


# Department API views


@api_view(http_method_names=["GET"])
def get_departments_with_additional_data_api_view(request: HttpRequest):
    response = []
    if request.user.is_superuser:
        departments = Department.objects.filter(active=True)
        for department in departments:
            male_count, female_count = 0, 0
            for f_department in FacultyDepartment.objects.filter(department=department):
                male_count += Student.objects.filter(
                    specialization__faculty_department=f_department,
                    gender="M",
                    is_expelled=False,
                    is_obsolete=False,
                ).count()
                female_count += Student.objects.filter(
                    specialization__faculty_department=f_department,
                    gender="F",
                    is_expelled=False,
                    is_obsolete=False,
                ).count()
            response.append(
                {
                    "id": department.id,
                    "name": department.name,
                    "students_count": male_count + female_count,
                    "male_count": male_count,
                    "female_count": female_count,
                }
            )
        return Response(response)
    else:
        response = []
        high_school = HighSchool.objects.get(manager__user=request.user)
        departments = FacultyDepartment.objects.filter(
            high_school_faculty__high_school=high_school
        )
        for department in departments:
            male_count = Student.objects.filter(
                specialization__faculty_department=department,
                gender="M",
                is_expelled=False,
                is_obsolete=False,
            ).count()
            female_count = Student.objects.filter(
                specialization__faculty_department=department,
                gender="F",
                is_expelled=False,
                is_obsolete=False,
            ).count()
            response.append(
                {
                    "id": department.department.id,
                    "name": department.department.name,
                    "faculty": department.high_school_faculty.faculty.name,
                    "specializations_count": DepartmentSpecialization.objects.filter(
                        faculty_department=department
                    ).count(),
                    "students_count": male_count + female_count,
                    "male_count": male_count,
                    "female_count": female_count,
                }
            )
        return Response(response)


@api_view(http_method_names=["GET"])
def remove_specialization_from_department_api_view(
    request: HttpRequest, department_specialization_id: int
):
    if DepartmentSpecialization.objects.filter(
        id=department_specialization_id
    ).exists():
        DepartmentSpecialization.objects.get(id=department_specialization_id).delete()
    else:
        return Response(
            {"detail": "Department specialization doesn't exist"}, status=404
        )
    return Response({"detail": "Success"})


@api_view(http_method_names=["POST"])
@validate_payload(keys=["high_school", "faculty", "departments"])
def create_faculty_departments_api_view(request: HttpRequest):
    if HighSchool.objects.filter(id=request.data["high_school"]).exists():
        high_school = HighSchool.objects.get(id=request.data["high_school"])
    else:
        return Response({"detail": "High school doesn't exist"}, status=404)

    if Faculty.objects.filter(id=request.data["faculty"]).exists():
        faculty = Faculty.objects.get(id=request.data["faculty"])
    else:
        return Response({"detail": "Faculty doesn't exist"}, status=404)

    if HighSchoolFaculty.objects.filter(high_school=high_school, faculty=faculty):
        high_school_faculty = HighSchoolFaculty.objects.get(
            high_school=high_school, faculty=faculty
        )
    else:
        return Response({"detail": "High school faculty doesn't exist"}, status=404)

    for department_id in request.data["departments"]:
        if Department.objects.filter(id=department_id).exists():
            department = Department.objects.get(id=department_id)
            if not FacultyDepartment.objects.filter(
                high_school_faculty=high_school_faculty, department=department
            ).exists():
                FacultyDepartment.objects.create(
                    high_school_faculty=high_school_faculty, department=department
                )
    return Response({"detail": "Success"})


class DepartmentListCreateAPIView(ListCreateAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    lookup_field = "id"


class DepartmentRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    lookup_field = "id"

    def delete(self, request: HttpRequest, id: int):
        instance = self.get_object()
        instance.active = False
        instance.save()
        return Response({"detail": "Success"})


# Degree API views


@api_view(http_method_names=["GET"])
def get_degrees_with_additional_data_api_view(request: HttpRequest):
    response = []
    degrees = Degree.objects.all()
    if request.user.is_superuser:

        for degree in degrees:
            male_count = Student.objects.filter(
                specialization__specialization__degree=degree,
                gender="M",
                is_expelled=False,
                is_obsolete=False,
            ).count()
            female_count = Student.objects.filter(
                specialization__specialization__degree=degree,
                gender="F",
                is_expelled=False,
                is_obsolete=False,
            ).count()

            response.append(
                {
                    "id": degree.id,
                    "name": degree.name,
                    "duration": degree.duration,
                    "students_count": male_count + female_count,
                    "male_count": male_count,
                    "female_count": female_count,
                }
            )
        return Response(response)
    else:
        # FIXME
        return Response(response)


class DegreeListCreateAPIView(ListCreateAPIView):
    queryset = Degree.objects.all()
    serializer_class = DegreeSerializer
    lookup_field = "id"


class DegreeRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Degree.objects.all()
    serializer_class = DegreeSerializer
    lookup_field = "id"


# Classificator API views


@api_view(http_method_names=["GET"])
def get_classificators_with_additional_data_api_view(request: HttpRequest):
    response = []
    classificators = Classificator.objects.all()
    if request.user.is_superuser:

        for classificator in classificators:
            male_count = Student.objects.filter(
                specialization__specialization__classificator=classificator,
                gender="M",
                is_expelled=False,
                is_obsolete=False,
            ).count()
            female_count = Student.objects.filter(
                specialization__specialization__classificator=classificator,
                gender="F",
                is_expelled=False,
                is_obsolete=False,
            ).count()

            response.append(
                {
                    "id": classificator.id,
                    "name": classificator.name,
                    "students_count": male_count + female_count,
                    "male_count": male_count,
                    "female_count": female_count,
                }
            )
        return Response(response)
    else:
        # FIXME
        return Response(response)


class ClassificatorListCreateAPIView(ListCreateAPIView):
    queryset = Classificator.objects.all()
    serializer_class = ClassificatorSerializer
    lookup_field = "id"


class ClassificatorRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Classificator.objects.all()
    serializer_class = ClassificatorSerializer
    lookup_field = "id"


# Specialization API views


@api_view(http_method_names=["GET"])
def get_specializations_with_additional_data_api_view(request: HttpRequest):
    response = []
    if request.user.is_superuser:
        specializations = Specialization.objects.filter(active=True)
        for specialization in specializations:
            male_count = Student.objects.filter(
                specialization__specialization=specialization,
                gender="M",
                is_expelled=False,
                is_obsolete=False,
            ).count()
            female_count = Student.objects.filter(
                specialization__specialization=specialization,
                gender="F",
                is_expelled=False,
                is_obsolete=False,
            ).count()

            response.append(
                {
                    "id": specialization.id,
                    "name": specialization.name,
                    "classificator": (
                        specialization.classificator.name
                        if specialization.classificator
                        else "Ýok"
                    ),
                    "students_count": male_count + female_count,
                    "male_count": male_count,
                    "female_count": female_count,
                }
            )
        return Response(response)
    else:
        response = []
        high_school = HighSchool.objects.get(manager__user=request.user)
        specializations = DepartmentSpecialization.objects.filter(
            faculty_department__high_school_faculty__high_school=high_school
        )
        for specialization in specializations:
            male_count = Student.objects.filter(
                specialization=specialization,
                gender="M",
                is_expelled=False,
                is_obsolete=False,
            ).count()
            female_count = Student.objects.filter(
                specialization=specialization,
                gender="F",
                is_expelled=False,
                is_obsolete=False,
            ).count()
            response.append(
                {
                    "id": specialization.specialization.id,
                    "name": specialization.specialization.name,
                    "department": specialization.faculty_department.department.name,
                    "classificator": (
                        specialization.specialization.classificator.name
                        if specialization.specialization.classificator
                        else "Ýok"
                    ),
                    "students_count": male_count + female_count,
                    "male_count": male_count,
                    "female_count": female_count,
                }
            )
        return Response(response)


@api_view(http_method_names=["POST"])
@validate_payload(keys=["high_school", "department", "specializations"])
def create_department_specializations_api_view(request: HttpRequest):
    if HighSchool.objects.filter(id=request.data["high_school"]).exists():
        high_school = HighSchool.objects.get(id=request.data["high_school"])
    else:
        return Response({"detail": "High school doesn't exist"}, status=404)

    if Department.objects.filter(id=request.data["department"]).exists():
        department = Department.objects.get(id=request.data["department"])
    else:
        return Response({"detail": "Faculty doesn't exist"}, status=404)

    if FacultyDepartment.objects.filter(
        high_school_faculty__high_school=high_school, department=department
    ):
        faculty_department = FacultyDepartment.objects.get(
            high_school_faculty__high_school=high_school, department=department
        )
    else:
        return Response({"detail": "Faculty department doesn't exist"}, status=404)

    for specialization_id in request.data["specializations"]:
        if Specialization.objects.filter(id=specialization_id).exists():
            specialization = Specialization.objects.get(id=specialization_id)
            if not DepartmentSpecialization.objects.filter(
                faculty_department=faculty_department, specialization=specialization
            ).exists():
                DepartmentSpecialization.objects.create(
                    faculty_department=faculty_department, specialization=specialization
                )
    return Response({"detail": "Success"})


@api_view(http_method_names=["PUT"])
@validate_payload(keys=["name", "abbreviation", "degree"])
def put_specialization_api_view(request: HttpRequest, id: int):

    if Specialization.objects.filter(id=id).exists():
        specialization = Specialization.objects.get(id=id)
    else:
        return Response({"detail": "Specialization doesn't exist"}, status=404)

    specialization.name = request.data["name"]
    specialization.abbreviation = request.data["abbreviation"]
    if request.data.get("classificator", False):
        if Classificator.objects.filter(id=request.data["classificator"]).exists():
            specialization.classificator = Classificator.objects.get(
                id=request.data["classificator"]
            )
        else:
            specialization.save()
            return Response({"detail": "Classificator doesn't exist"}, status=404)
    else:
        specialization.classificator = None
    if Degree.objects.filter(id=request.data["degree"]).exists():
        specialization.degree = Degree.objects.get(id=request.data["degree"])
    else:
        specialization.save()
        return Response({"detail": "Degree doesn't exist"}, status=404)
    specialization.save()

    return Response({"detail": "Success", "id": specialization.id})


class SpecializationListCreateAPIView(ListCreateAPIView):
    queryset = Specialization.objects.all()
    serializer_class = SpecializationSerializer
    lookup_field = "id"


class SpecializationRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Specialization.objects.all()
    serializer_class = SpecializationSerializer
    lookup_field = "id"

    def delete(self, request: HttpRequest, id: int):
        instance = self.get_object()
        instance.active = False
        instance.save()
        return Response({"detail": "Success"})


# Student API views


@api_view(http_method_names=["POST"])
@validate_payload(keys=["high_school_id"])
@validate_files(keys=["excel"])
def import_students_from_excel_api_view(request: HttpRequest):
    dataframe = pd.read_excel(request.FILES["excel"])
    invalid_fields = []
    if HighSchool.objects.filter(id=request.POST["high_school_id"]).exists():
        high_school = HighSchool.objects.get(id=request.POST["high_school_id"])
    else:
        return Response({"detail": "High school doesn't exist"})

    for index, row in dataframe.iterrows():
        row_validation = True
        row_status = validate_not_null_field(row, ["T/B", "Harby borç", "Bellikler"])
        if not row_status[0]:
            invalid_fields.append(
                f"Setir №{index + 1}: '{','.join(row_status[1])}' meýdançasy boş bolup bilmez"
            )
        else:
            full_name = row["F.A.Aa"]
            if type(row["Doglan senesi"]) == datetime.datetime:
                birth_date = row["Doglan senesi"]
            elif type(row["Doglan senesi"]) == str:
                try:
                    birth_date = datetime.datetime.strptime(
                        row["Doglan senesi"], "%d.%M.%Y"
                    )
                except:
                    invalid_fields.append(
                        f"Setir №{index + 1}: 'Okuwa giren senesi' meýdançasynda ýalňyşlyk goýberildi"
                    )
                    row_validation = False
            else:
                birth_date = row["Doglan senesi"].to_pydatetime()

            if row["Jynsy"] in ("Oglan", "Gyz"):
                gender = "M" if row["Jynsy"] == "Oglan" else "F"
            else:
                invalid_fields.append(
                    f"Setir №{index + 1}: 'Jynsy' meýdançasynda ýalňyşlyk goýberildi"
                )
                row_validation = False

            if Region.objects.filter(name=row["Welaýaty"]).exists():
                region = Region.objects.get(name=row["Welaýaty"])
            else:
                invalid_fields.append(
                    f"Setir №{index + 1}: 'Welaýaty' meýdançasynda ýalňyşlyk goýberildi"
                )
                row_validation = False

            if Nationality.objects.filter(name=row["Milleti"]).exists():
                nationality = Nationality.objects.get(name=row["Milleti"])
            else:
                invalid_fields.append(
                    f"Setir №{index + 1}: 'Milleti' meýdançasynda ýalňyşlyk goýberildi"
                )
                row_validation = False

            if Country.objects.filter(name=row["Ýurdy"]).exists():
                country = Country.objects.get(name=row["Ýurdy"])
            else:
                invalid_fields.append(
                    f"Setir №{index + 1}: 'Milleti' meýdançasynda ýalňyşlyk goýberildi"
                )
                row_validation = False

            if DepartmentSpecialization.objects.filter(
                specialization__name=row["Hünari"],
                faculty_department__high_school_faculty__high_school=high_school,
            ):
                specialization = DepartmentSpecialization.objects.get(
                    specialization__name=row["Hünari"],
                    faculty_department__high_school_faculty__high_school=high_school,
                )
            else:
                invalid_fields.append(
                    f"Setir №{index + 1}: 'Hünäri' meýdançasynda ýalňyşlyk goýberildi"
                )
                row_validation = False
            # FIXME
            if (
                type(row["Kursy"]) == int
                or type(row["Kursy"]) == float
                or type(row["Kursy"]) == str
            ):
                if type(row["Kursy"]) == float:
                    course = str(int(row["Kursy"]))
                else:
                    course = str(row["Kursy"])
            else:
                invalid_fields.append(
                    f"Setir №{index + 1}: 'Kursy' meýdançasynda ýalňyşlyk goýberildi"
                )
                row_validation = False

            if row["Töleg görnüşi"] in ("Tölegli", "Býudjet"):
                payment_type = "P" if row["Töleg görnüşi"] == "Tölegli" else "B"
            else:
                invalid_fields.append(
                    f"Setir №{index + 1}: 'Töleg görnüşi' meýdançasynda ýalňyşlyk goýberildi"
                )
                row_validation = False

            family_statuses = {
                "Hossarly": "FR",
                "Ýarym ýetim": "HO",
                "Doly ýetim": "CO",
                "Ýetimler öýünde ösen": "OE",
            }
            if row["Maşgala ýagdaýy"] in family_statuses.keys():
                family_status = family_statuses[row["Maşgala ýagdaýy"]]
            else:
                invalid_fields.append(
                    f"Setir №{index + 1}: 'Maşgala ýagdaýy' meýdançasynda ýalňyşlyk goýberildi"
                )
                row_validation = False

            if type(row["Ýazgyda duran salgysy"]) == str:
                registered_place = row["Ýazgyda duran salgysy"]
            else:
                invalid_fields.append(
                    f"Setir №{index + 1}: 'Ýazgyda duran salgysy' meýdançasynda ýalňyşlyk goýberildi"
                )
                row_validation = False

            if (
                type(row["Öý, iş, mobil telefony"]) == str
                or type(row["Öý, iş, mobil telefony"]) == int
                or type(row["Öý, iş, mobil telefony"]) == float
            ):
                if type(row["Öý, iş, mobil telefony"]) == float:
                    phone_number = str(int(row["Öý, iş, mobil telefony"]))
                else:
                    phone_number = str(row["Öý, iş, mobil telefony"])
            else:
                invalid_fields.append(
                    f"Setir №{index + 1}: 'Öý, iş, mobil telefony' meýdançasynda ýalňyşlyk goýberildi"
                )
                row_validation = False

            if type(row["Pasport seriýasy, belgisi"]) == str:
                passport = row["Pasport seriýasy, belgisi"]
            else:
                invalid_fields.append(
                    f"Setir №{index + 1}: 'Pasport seriýasy, belgisi' meýdançasynda ýalňyşlyk goýberildi"
                )
                row_validation = False

            if type(row["Okuwa giren senesi"]) == datetime.datetime:
                admission_date = row["Okuwa giren senesi"]
            elif type(row["Okuwa giren senesi"]) == str:
                try:
                    admission_date = datetime.datetime.strptime(
                        row["Okuwa giren senesi"], "%d.%M.%Y"
                    )
                except:
                    invalid_fields.append(
                        f"Setir №{index + 1}: 'Okuwa giren senesi' meýdançasynda ýalňyşlyk goýberildi"
                    )
                    row_validation = False
            else:
                admission_date = row["Okuwa giren senesi"].to_pydatetime()

            if row_validation:
                if not Student.objects.filter(
                    high_school=high_school,
                    full_name=full_name,
                    specialization=specialization,
                    passport=passport,
                ).exists():
                    student = Student.objects.create(
                        full_name=full_name,
                        gender=gender,
                        family_status=family_status,
                        payment_type=payment_type,
                        nationality=nationality,
                        country=country,
                        region=region,
                        study_year=course,
                        high_school=high_school,
                        specialization=specialization,
                        birth_date=birth_date,
                        admission_date=admission_date,
                        registered_place=registered_place,
                        phone_number=phone_number,
                        passport=passport,
                    )
                    if not row.isnull()["Bellikler"]:
                        student.label = row["Bellikler"]
                    if not row.isnull()["Harby borç"]:
                        student.military_service = row["Harby borç"]
                    student.save()
                else:
                    invalid_fields.append(
                        f"Setir №{index + 1}: '{full_name}' atly talyp eýýäm maglumat goruna girizilen"
                    )
    if len(invalid_fields) > 0:
        print("its me")
        return Response(
            {
                "detail": "Success, but there are some mistakes",
                "mistakes": invalid_fields,
            }
        )
    return Response(
        {
            "detail": "Success",
        }
    )


@api_view(http_method_names=["GET"])
def get_students_with_additional_data_api_view(request: HttpRequest):

    if request.user.is_superuser:
        students = Student.objects.filter(
            active=True, is_expelled=False, is_obsolete=False
        )
        response = filter_by_query(students, request.GET)
        return Response(StudentAdditionalSerializer(response, many=True).data)
    else:
        students = Student.objects.filter(
            high_school=HighSchool.objects.get(manager__user=request.user),
            active=True,
            is_expelled=False,
            is_obsolete=False,
        )
        return Response(
            [
                {
                    "id": student.id,
                    "full_name": student.full_name,
                    "faculty": student.specialization.faculty_department.high_school_faculty.faculty.name,
                    "study_year": student.study_year,
                }
                for student in students
            ]
        )


@api_view(http_method_names=["GET"])
def get_graduates_with_additional_data_api_view(request: HttpRequest):
    if request.user.is_superuser:
        students = Student.objects.filter(
            active=True, is_expelled=False, is_obsolete=True
        )
        return Response(GraduateAdditionalSerializer(students, many=True).data)
    else:
        return Response({"detail": "Permission denied"}, status=403)


class StudentListAPIView(ListAPIView):
    queryset = Student.objects.filter(is_expelled=False)
    serializer_class = StudentSerializer
    lookup_field = "id"


class StudentInfoAPIView(RetrieveAPIView):
    queryset = Student.objects.filter(is_expelled=False)
    serializer_class = StudentInfoSerializer
    lookup_field = "id"


class GraduateInfoAPIView(RetrieveAPIView):
    queryset = Student.objects.filter(is_obsolete=True)
    serializer_class = GraduateInfoSerializer
    lookup_field = "id"


class NeutralStudentInfoAPIView(RetrieveAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentInfoSerializer
    lookup_field = "id"


class StudentRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    lookup_field = "id"

    def delete(self, request: HttpRequest, id: int):
        instance = self.get_object()
        instance.active = False
        instance.save()
        return Response({"detail": "Success"})


# Nationalization API views


class NationalityListCreateAPIView(ListCreateAPIView):
    queryset = Nationality.objects.all()
    serializer_class = NationalitySerializer
    lookup_field = "id"


class NationalityRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Nationality.objects.all()
    serializer_class = NationalitySerializer
    lookup_field = "id"


@api_view(http_method_names=["GET"])
def get_nationalizations_with_additional_data_api_view(request: HttpRequest):
    response = []
    nationalities = Nationality.objects.all()
    if request.user.is_superuser:

        for nationality in nationalities:
            male_count = Student.objects.filter(
                nationality=nationality, gender="M"
            ).count()
            female_count = Student.objects.filter(
                nationality=nationality, gender="F"
            ).count()

            response.append(
                {
                    "id": nationality.id,
                    "name": nationality.name,
                    "students_count": male_count + female_count,
                    "male_count": male_count,
                    "female_count": female_count,
                }
            )
        return Response(response)
    else:
        high_school = HighSchool.objects.get(manager__user=request.user)
        for nationality in nationalities:
            male_count = Student.objects.filter(
                nationality=nationality,
                gender="M",
                high_school=high_school,
            ).count()
            female_count = Student.objects.filter(
                nationality=nationality,
                gender="F",
                high_school=high_school,
            ).count()

            response.append(
                {
                    "id": nationality.id,
                    "name": nationality.name,
                    "students_count": male_count + female_count,
                    "male_count": male_count,
                    "female_count": female_count,
                }
            )
        return Response(response)


# Country API views


class CountryListCreateAPIView(ListCreateAPIView):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    lookup_field = "id"


class CountryRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    lookup_field = "id"


@api_view(http_method_names=["GET"])
def get_countries_with_additional_data_api_view(request: HttpRequest):
    response = []
    countries = Country.objects.all()
    if request.user.is_superuser:
        for country in countries:
            male_count = Student.objects.filter(
                country=country, gender="M", is_expelled=False, is_obsolete=False
            ).count()
            female_count = Student.objects.filter(
                country=country, gender="F", is_expelled=False, is_obsolete=False
            ).count()

            response.append(
                {
                    "id": country.id,
                    "name": country.name,
                    "students_count": male_count + female_count,
                    "male_count": male_count,
                    "female_count": female_count,
                }
            )
        return Response(response)
    else:
        high_school = HighSchool.objects.get(manager__user=request.user)
        for country in countries:
            male_count = Student.objects.filter(
                country=country,
                gender="M",
                high_school=high_school,
                is_expelled=False,
                is_obsolete=False,
            ).count()
            female_count = Student.objects.filter(
                country=country,
                gender="F",
                high_school=high_school,
                is_expelled=False,
                is_obsolete=False,
            ).count()

            response.append(
                {
                    "id": country.id,
                    "name": country.name,
                    "students_count": male_count + female_count,
                    "male_count": male_count,
                    "female_count": female_count,
                }
            )
        return Response(response)


# Region API views


class RegionListCreateAPIView(ListCreateAPIView):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer
    lookup_field = "id"


class RegionRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer
    lookup_field = "id"


@api_view(http_method_names=["GET"])
def get_regions_with_additional_data_api_view(request: HttpRequest):
    response = []
    regions = Region.objects.all()
    if request.user.is_superuser:
        for region in regions:
            male_count = Student.objects.filter(
                region=region, gender="M", is_expelled=False, is_obsolete=False
            ).count()
            female_count = Student.objects.filter(
                region=region, gender="F", is_expelled=False, is_obsolete=False
            ).count()

            response.append(
                {
                    "id": region.id,
                    "name": region.name,
                    "students_count": male_count + female_count,
                    "male_count": male_count,
                    "female_count": female_count,
                }
            )
        return Response(response)
    else:
        high_school = HighSchool.objects.get(manager__user=request.user)
        for region in regions:
            male_count = Student.objects.filter(
                region=region,
                gender="M",
                high_school=high_school,
                is_expelled=False,
                is_obsolete=False,
            ).count()
            female_count = Student.objects.filter(
                region=region,
                gender="F",
                high_school=high_school,
                is_expelled=False,
                is_obsolete=False,
            ).count()

            response.append(
                {
                    "id": region.id,
                    "name": region.name,
                    "students_count": male_count + female_count,
                    "male_count": male_count,
                    "female_count": female_count,
                }
            )
        return Response(response)


# Expulsion reason API views


class ExpulsionReasonListCreateAPIView(ListCreateAPIView):
    queryset = ExpulsionReason.objects.all()
    serializer_class = ExpulsionReasonSerializer
    lookup_field = "id"


class ExpulsionReasonRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = ExpulsionReason.objects.all()
    serializer_class = ExpulsionReasonSerializer
    lookup_field = "id"


# Expulsion request API views


class ExpulsionRequestListCreateAPIView(ListCreateAPIView):
    queryset = ExpulsionRequest.objects.all()
    serializer_class = ExpulsionRequestSerializer
    lookup_field = "id"


class ExpulsionRequestRetrieveAPIView(RetrieveAPIView):
    queryset = ExpulsionRequest.objects.all()
    serializer_class = ExpulsionRequestSerializer
    lookup_field = "id"


@api_view(http_method_names=["GET"])
def get_expelled_students_api_view(request: HttpRequest):
    response = []
    students = Student.objects.filter(
        is_expelled=True, high_school=HighSchool.objects.get(manager__user=request.user)
    )
    for student in students:
        if ExpulsionRequest.objects.filter(
            student=student,
            verdict="C",
            is_obsolete=False,
        ).exists():
            expulsion_request = ExpulsionRequest.objects.filter(
                student=student,
                verdict="C",
                is_obsolete=False,
            ).last()
            response.append(
                {
                    "id": student.id,
                    "request_id": expulsion_request.id,
                    "full_name": student.full_name,
                    "expulsion_date": expulsion_request.verdict_date.astimezone(
                        pytz.timezone("Asia/Ashgabat")
                    ).strftime("%d.%m.%Y %H:%M:%S"),
                    "study_year": student.study_year,
                }
            )
    return Response(response)


@api_view(http_method_names=["GET"])
def get_expelled_student_api_view(request: HttpRequest, student_id: int):
    if Student.objects.filter(
        is_expelled=True,
        high_school=HighSchool.objects.get(manager__user=request.user),
        id=student_id,
    ).exists():
        student = Student.objects.get(
            is_expelled=True,
            high_school=HighSchool.objects.get(manager__user=request.user),
            id=student_id,
        )
    else:
        return Response({"detail": "Expelled student not found"}, status=404)

    if ExpulsionRequest.objects.filter(
        student=student,
        verdict="C",
        is_obsolete=False,
    ).exists():
        expulsion_request = ExpulsionRequest.objects.filter(
            student=student,
            verdict="C",
            is_obsolete=False,
        ).last()
        return Response(ExpelledStudentInfoSerializer(student).data)
    return Response({"detail": "Expelled student not found"}, status=404)


# Reinstate request API views


class ReinstateRequestListCreateAPIView(ListCreateAPIView):
    queryset = ReinstateRequest.objects.all()
    serializer_class = ReinstateRequestSerializer
    lookup_field = "id"


class ReinstateRequestRetrieveAPIView(RetrieveAPIView):
    queryset = ReinstateRequest.objects.all()
    serializer_class = ReinstateRequestSerializer
    lookup_field = "id"


# Statement special API views


@api_view(http_method_names=["GET"])
def get_statements_api_view(request: HttpRequest):
    response = []

    for expulsion_request in ExpulsionRequest.objects.filter(is_obsolete=False):
        if expulsion_request.verdict:
            if expulsion_request.verdict == "C":
                verdict = "Kabul edildi"
            else:
                verdict = "Ret edildi"
        else:
            verdict = "Barlagda"

        response.append(
            {
                "id": expulsion_request.id,
                "type": "Okuwdan boşatmak",
                "sender": HighSchool.objects.get(
                    manager__user=expulsion_request.sender
                ).name,
                "status": verdict,
                "request_date": expulsion_request.request_date.astimezone(
                    pytz.timezone("Asia/Ashgabat")
                ).strftime("%d.%m.%Y %H:%M:%S"),
            }
        )
    for reinstate_request in ReinstateRequest.objects.filter(is_obsolete=False):
        if reinstate_request.verdict:
            if reinstate_request.verdict == "C":
                verdict = "Kabul edildi"
            else:
                verdict = "Ret edildi"
        else:
            verdict = "Barlagda"

        response.append(
            {
                "id": reinstate_request.id,
                "type": "Okuwy dikeltmek",
                "sender": HighSchool.objects.get(
                    manager__user=reinstate_request.sender
                ).name,
                "status": verdict,
                "request_date": reinstate_request.request_date.astimezone(
                    pytz.timezone("Asia/Ashgabat")
                ).strftime("%d.%m.%Y %H:%M:%S"),
            }
        )
    response.sort(key=lambda e: e["request_date"])
    response.reverse()
    return Response(response)


@api_view(http_method_names=["GET"])
def get_statement_api_view(
    request: HttpRequest, statement_id: int, statement_type: str
):

    if statement_type == "expulsion":
        if ExpulsionRequest.objects.filter(id=statement_id, is_obsolete=False).exists():
            statement = ExpulsionRequest.objects.get(id=statement_id)
        else:
            return Response({"detail": "Expulsion request not found"}, status=404)
    elif statement_type == "reinstate":
        if ReinstateRequest.objects.filter(id=statement_id, is_obsolete=False).exists():
            statement = ReinstateRequest.objects.get(id=statement_id)
        else:
            return Response({"detail": "Reinstate request not found"}, status=404)
    else:
        return Response({"detail": "Invalid statement type"}, status=400)

    if statement.verdict:
        if statement.verdict == "C":
            verdict = "Kabul edildi"
        else:
            verdict = "Ret edildi"
    else:
        verdict = "Barlagda"

    response = (
        {
            "id": statement.id,
            "type": statement_type,
            "reason": statement.reason.name,
            "student": statement.student.id,
            "sender": HighSchool.objects.get(manager__user=statement.sender).name,
            "status": verdict,
            "detail": statement.detail,
            "request_date": statement.request_date.astimezone(
                pytz.timezone("Asia/Ashgabat")
            ).strftime("%d.%m.%Y %H:%M:%S"),
        }
        if statement_type == "expulsion"
        else {
            "id": statement.id,
            "type": statement_type,
            "student": statement.student.id,
            "sender": HighSchool.objects.get(manager__user=statement.sender).name,
            "status": verdict,
            "detail": statement.detail,
            "request_date": statement.request_date.astimezone(
                pytz.timezone("Asia/Ashgabat")
            ).strftime("%d.%m.%Y %H:%M:%S"),
        }
    )
    return Response(response)


@api_view(http_method_names=["GET"])
def verdict_statement_api_view(
    request: HttpRequest, statement_id: int, statement_type: str, verdict: str
):

    if statement_type == "expulsion":
        if ExpulsionRequest.objects.filter(id=statement_id, is_obsolete=False).exists():
            statement = ExpulsionRequest.objects.get(id=statement_id)
        else:
            return Response({"detail": "Expulsion request not found"}, status=404)
    elif statement_type == "reinstate":
        if ReinstateRequest.objects.filter(id=statement_id, is_obsolete=False).exists():
            statement = ReinstateRequest.objects.get(id=statement_id)
        else:
            return Response({"detail": "Reinstate request not found"}, status=404)
    else:
        return Response({"detail": "Invalid statement type"}, status=400)

    if verdict == "confirm":
        statement.confirm()
    elif verdict == "reject":
        statement.reject()
    else:
        return Response({"detail": "Invalid verdict"}, status=400)
    return Response({"detail": "Success"})


@api_view(http_method_names=["POST"])
@validate_payload(["obj_name"])
def mark_as_viewed_api_view(request: HttpRequest, obj_id: int):
    object_name = request.data["obj_name"]
    if object_name == "expulsion":
        if ExpulsionRequest.objects.filter(id=obj_id).exists():
            obj = ExpulsionRequest.objects.get(id=obj_id)
        else:
            return Response({"detail": "Expulsion request not found"}, status=404)
    elif object_name == "reinstate":
        if ReinstateRequest.objects.filter(id=obj_id).exists():
            obj = ReinstateRequest.objects.get(id=obj_id)
        else:
            return Response({"detail": "Reinstate request not found"}, status=404)

    obj.viewed_by.add(request.user)
    return Response({"detail": "Success"})


# Diploma API views


@api_view(http_method_names=["GET"])
def get_diploma_request_by_user_api_view(request: HttpRequest):
    if DiplomaRequest.objects.filter(sender=request.user, is_obsolete=False).exists():
        if (
            DiplomaRequest.objects.get(sender=request.user).verdict == "C"
            or DiplomaRequest.objects.get(sender=request.user).verdict == None
        ):
            diploma_request = DiplomaRequest.objects.get(sender=request.user)
        else:
            return Response({"null": True})
    else:
        return Response({"null": True})
    return Response(advanced_diploma_serializer(diploma_request))


@api_view(http_method_names=["GET"])
def get_diploma_request_by_id_api_view(request: HttpRequest, diploma_request_id: int):
    if DiplomaRequest.objects.filter(is_obsolete=False, id=diploma_request_id).exists():
        diploma_request = DiplomaRequest.objects.get(id=diploma_request_id)
    else:
        return Response({"null": True})
    return Response(advanced_diploma_serializer(diploma_request))


@api_view(http_method_names=["GET"])
def get_diploma_request_by_high_school_api_view(
    request: HttpRequest, high_school_id: int
):
    if HighSchool.objects.filter(id=high_school_id).exists():
        high_school = HighSchool.objects.get(id=high_school_id)
    else:
        return Response({"detail": "High school not found"}, status=404)

    if DiplomaRequest.objects.filter(
        is_obsolete=False, sender=high_school.manager.user
    ).exists():
        diploma_request = DiplomaRequest.objects.get(
            is_obsolete=False, sender=high_school.manager.user
        )
    else:
        return Response({"null": True})
    return Response(advanced_diploma_serializer(diploma_request))


@api_view(http_method_names=["POST"])
@validate_payload(keys=["simple_diploma_count", "honor_diploma_count"])
def create_diploma_request_api_view(request: HttpRequest):
    DiplomaRequest.objects.create(
        simple_diploma_count=request.data["simple_diploma_count"],
        honor_diploma_count=request.data["honor_diploma_count"],
        sender=request.user,
        allowed_until=timezone.now() + datetime.timedelta(days=30),
    )
    return Response({"detail": "Success"})


@api_view(http_method_names=["POST"])
@validate_payload(
    keys=[
        "simple_diploma_count",
        "honor_diploma_count",
        "two_year_work_off",
        "died",
        "went_abroad",
        "other_reasons",
    ]
)
def update_diploma_request_api_view(request: HttpRequest, diploma_request_id: int):
    if DiplomaRequest.objects.filter(id=diploma_request_id).exists():
        diploma_request = DiplomaRequest.objects.get(id=diploma_request_id)
    else:
        return Response({"detail": "Diploma request not found"}, status=404)
    if (
        request.data["simple_diploma_count"] > 0
        or request.data["honor_diploma_count"] > 0
    ):
        DiplomaRequestAction.objects.create(
            update_simple_to=request.data["simple_diploma_count"],
            update_honor_to=request.data["honor_diploma_count"],
            diploma_request=diploma_request,
        )
    if (
        request.data["two_year_work_off"] > 0
        or request.data["died"] > 0
        or request.data["went_abroad"]
        or request.data["other_reasons"] > 0
    ):
        DiplomaReport.objects.create(
            two_year_work_off=request.data["two_year_work_off"],
            died=request.data["died"],
            went_abroad=request.data["went_abroad"],
            other_reasons=request.data["other_reasons"],
            diploma_request=diploma_request,
        )
    diploma_request.clear_viewed_by()
    return Response({"detail": "Success"})


@api_view(http_method_names=["GET"])
def get_diplomas_for_table_api_view(request: HttpRequest):
    response = []
    for diploma_request in DiplomaRequest.objects.filter(
        is_obsolete=False, verdict__in=["C", None]
    ):
        response.append(
            {
                "id": diploma_request.id,
                "sender": HighSchool.objects.get(
                    manager__user=diploma_request.sender
                ).name,
            }
        )
    return Response(response)


@api_view(http_method_names=["GET"])
def get_diploma_request_actions_api_view(request: HttpRequest):
    response = []
    for diploma_request_action in DiplomaRequestAction.objects.filter(verdict="C"):
        if (
            not diploma_request_action.diploma_request.is_obsolete
            and not diploma_request_action.diploma_request.verdict == "R"
        ):
            response.append(
                {
                    "id": diploma_request_action.id,
                    "verdict_date": (
                        diploma_request_action.verdict_date.astimezone(
                            pytz.timezone("Asia/Ashgabat")
                        ).strftime("%d.%m.%Y %H:%M:%S")
                        if diploma_request_action.verdict_date
                        else None
                    ),
                    "sender": HighSchool.objects.get(
                        manager__user=diploma_request_action.diploma_request.sender
                    ).abbreviation,
                    "count": diploma_request_action.update_honor_to
                    + diploma_request_action.update_simple_to,
                    "type": "up",
                }
            )
    for diploma_report in DiplomaReport.objects.filter(verdict="C"):
        if (
            not diploma_report.diploma_request.is_obsolete
            and not diploma_report.diploma_request.verdict == "R"
        ):
            response.append(
                {
                    "id": diploma_report.id,
                    "verdict_date": (
                        diploma_report.verdict_date.astimezone(
                            pytz.timezone("Asia/Ashgabat")
                        ).strftime("%d.%m.%Y %H:%M:%S")
                        if diploma_report.verdict_date
                        else None
                    ),
                    "sender": HighSchool.objects.get(
                        manager__user=diploma_report.diploma_request.sender
                    ).abbreviation,
                    "count": diploma_report.two_year_work_off
                    + diploma_report.died
                    + diploma_report.went_abroad
                    + diploma_report.other_reasons,
                    "type": "down",
                }
            )
    return Response(response)


@api_view(http_method_names=["GET"])
def get_high_school_diploma_request_actions_api_view(
    request: HttpRequest, diploma_request_id: int
):
    response = {"actions": [], "reports": []}
    if DiplomaRequest.objects.filter(id=diploma_request_id).exists():
        diploma_request = DiplomaRequest.objects.get(id=diploma_request_id)
    else:
        return Response({"detail": "Diploma request not found"}, status=404)

    diploma_request.viewed_by.add(request.user)
    diploma_request.save()

    for diploma_request_action in DiplomaRequestAction.objects.filter(
        diploma_request=diploma_request
    ):

        response["actions"].append(
            {
                "id": diploma_request_action.id,
                "verdict": diploma_request_action.verdict,
                "request_date": diploma_request_action.request_date.astimezone(
                    pytz.timezone("Asia/Ashgabat")
                ).strftime("%d.%m.%Y %H:%M:%S"),
                "verdict_date": (
                    diploma_request_action.verdict_date.astimezone(
                        pytz.timezone("Asia/Ashgabat")
                    ).strftime("%d.%m.%Y %H:%M:%S")
                    if diploma_request_action.verdict_date
                    else None
                ),
                "sender": HighSchool.objects.get(
                    manager__user=diploma_request_action.diploma_request.sender
                ).abbreviation,
                "honor_diploma_count": diploma_request_action.update_honor_to,
                "simple_diploma_count": diploma_request_action.update_simple_to,
                "type": "up",
            }
        )
    for diploma_report in DiplomaReport.objects.filter(diploma_request=diploma_request):
        response["reports"].append(
            {
                "id": diploma_report.id,
                "verdict": diploma_report.verdict,
                "request_date": diploma_report.request_date.astimezone(
                    pytz.timezone("Asia/Ashgabat")
                ).strftime("%d.%m.%Y %H:%M:%S"),
                "verdict_date": (
                    diploma_report.verdict_date.astimezone(
                        pytz.timezone("Asia/Ashgabat")
                    ).strftime("%d.%m.%Y %H:%M:%S")
                    if diploma_report.verdict_date
                    else None
                ),
                "sender": HighSchool.objects.get(
                    manager__user=diploma_report.diploma_request.sender
                ).abbreviation,
                "two_year_work_off": diploma_report.two_year_work_off,
                "died": diploma_report.died,
                "went_abroad": diploma_report.went_abroad,
                "other_reasons": diploma_report.other_reasons,
                "type": "down",
            }
        )
    response["actions"].sort(key=lambda e: e["request_date"])
    response["reports"].sort(key=lambda e: e["request_date"])
    return Response(response)


@api_view(http_method_names=["GET"])
def submit_diploma_report_api_view(request: HttpRequest, diploma_report_id: int):
    response = {"actions": [], "reports": []}
    if DiplomaReport.objects.filter(id=diploma_report_id).exists():
        diploma_report = DiplomaReport.objects.get(id=diploma_report_id)
    else:
        return Response({"detail": "Diploma report not found"}, status=404)

    diploma_report.verdict = "C"
    diploma_report.verdict_date = timezone.now()
    diploma_report.save()

    return Response(response)


@api_view(http_method_names=["GET"])
def submit_diploma_action_api_view(request: HttpRequest, diploma_action_id: int):
    response = {"actions": [], "reports": []}
    if DiplomaRequestAction.objects.filter(id=diploma_action_id).exists():
        diploma_action = DiplomaRequestAction.objects.get(id=diploma_action_id)
    else:
        return Response({"detail": "Diploma action not found"}, status=404)

    diploma_action.verdict = "C"
    diploma_action.verdict_date = timezone.now()
    diploma_action.save()

    return Response(response)


@api_view(http_method_names=["GET"])
def verdict_diploma_request_api_view(
    request: HttpRequest, diploma_request_id: int, verdict: str
):
    if not verdict in ["C", "R"]:
        return Response({"detail": "Invalid verdict type"}, status=400)
    if DiplomaRequest.objects.filter(id=diploma_request_id).exists():
        diploma_request = DiplomaRequest.objects.get(id=diploma_request_id)
    else:
        return Response({"detail": "Diploma request not found"}, status=404)

    diploma_request.verdict = verdict.upper()
    diploma_request.verdict_date = timezone.now()
    diploma_request.save()

    return Response({"detail": "Success"})


class DiplomaRequestsAPIView(RetrieveUpdateDestroyAPIView):
    queryset = DiplomaRequest.objects.all()
    serializer_class = DiplomaRequestSerializer
    lookup_field = "id"

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_obsolete = True
        instance.save()
        return Response({"detail": "Success"})


# Teacher Statement


@api_view(http_method_names=["GET"])
def get_teacher_statement_by_user_api_view(request: HttpRequest):
    if TeacherStatement.objects.filter(sender=request.user, is_obsolete=False).exists():
        if (
            TeacherStatement.objects.get(sender=request.user).verdict == "C"
            or TeacherStatement.objects.get(sender=request.user).verdict == None
        ):
            teacher_statement = TeacherStatement.objects.get(sender=request.user)
        else:
            return Response({"null": True})
    else:
        return Response({"null": True})
    return Response(TeacherStatementSerializer(teacher_statement).data)


@api_view(http_method_names=["GET"])
def get_teacher_statement_by_id_api_view(
    request: HttpRequest, teacher_statement_id: int
):
    if TeacherStatement.objects.filter(
        is_obsolete=False, id=teacher_statement_id
    ).exists():
        teacher_statement = TeacherStatement.objects.get(id=teacher_statement_id)
    else:
        return Response({"null": True})

    teacher_statement.viewed_by.add(request.user)
    teacher_statement.save()
    return Response(TeacherStatementSerializer(teacher_statement).data)


@api_view(http_method_names=["POST"])
@validate_payload(
    keys=[
        "workload_1_25",
        "workload_1_00",
        "workload_0_75",
        "workload_0_50",
        "doctor_degree",
        "candidate_degree",
        "professor",
        "docent",
        "department_head",
        "professor_job",
        "docent_job",
        "senior_teachers",
        "teachers",
        "intern_teachers",
    ]
)
def create_teacher_statement_api_view(request: HttpRequest):
    TeacherStatement.objects.create(
        workload_1_25=request.data["workload_1_25"],
        workload_1_00=request.data["workload_1_00"],
        workload_0_75=request.data["workload_0_75"],
        workload_0_50=request.data["workload_0_50"],
        doctor_degree=request.data["doctor_degree"],
        candidate_degree=request.data["candidate_degree"],
        professor=request.data["professor"],
        docent=request.data["docent"],
        department_head=request.data["department_head"],
        professor_job=request.data["professor_job"],
        docent_job=request.data["docent_job"],
        senior_teachers=request.data["senior_teachers"],
        teachers=request.data["teachers"],
        intern_teachers=request.data["intern_teachers"],
        sender=request.user,
        allowed_until=timezone.now() + datetime.timedelta(days=30),
    )
    return Response({"detail": "Success"})


@api_view(http_method_names=["GET"])
def get_teacher_statements_for_table_api_view(request: HttpRequest):
    response = []
    for teacher_statement in TeacherStatement.objects.filter(
        is_obsolete=False,
    ):
        sender = HighSchool.objects.get(manager__user=teacher_statement.sender)
        if teacher_statement.verdict == "C":
            response.append(
                {
                    "id": teacher_statement.id,
                    "sender": sender.name,
                    "sender_abbr": sender.abbreviation,
                    "workload_1_25": teacher_statement.workload_1_25,
                    "workload_1_00": teacher_statement.workload_1_00,
                    "workload_0_75": teacher_statement.workload_0_75,
                    "workload_0_50": teacher_statement.workload_0_50,
                    "doctor_degree": teacher_statement.doctor_degree,
                    "candidate_degree": teacher_statement.candidate_degree,
                    "professor": teacher_statement.professor,
                    "docent": teacher_statement.docent,
                    "department_head": teacher_statement.department_head,
                    "professor_job": teacher_statement.professor_job,
                    "docent_job": teacher_statement.docent_job,
                    "senior_teachers": teacher_statement.senior_teachers,
                    "teachers": teacher_statement.teachers,
                    "intern_teachers": teacher_statement.intern_teachers,
                }
            )
        else:
            response.append(
                {
                    "id": teacher_statement.id,
                    "sender": sender.name,
                    "sender_abbr": sender.abbreviation,
                    "workload_1_25": 0,
                    "workload_1_00": 0,
                    "workload_0_75": 0,
                    "workload_0_50": 0,
                    "doctor_degree": 0,
                    "candidate_degree": 0,
                    "professor": 0,
                    "docent": 0,
                    "department_head": 0,
                    "professor_job": 0,
                    "docent_job": 0,
                    "senior_teachers": 0,
                    "teachers": 0,
                    "intern_teachers": 0,
                }
            )

    return Response(response)


class TeacherStatementsAPIView(RetrieveUpdateDestroyAPIView):
    queryset = TeacherStatement.objects.all()
    serializer_class = TeacherStatementSerializer
    lookup_field = "id"

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_obsolete = True
        instance.save()
        return Response({"detail": "Success"})


@api_view(http_method_names=["GET"])
def verdict_teacher_statement_api_view(
    request: HttpRequest, teacher_statement_id: int, verdict: str
):
    if not verdict in ["C", "R"]:
        return Response({"detail": "Invalid verdict type"}, status=400)
    if TeacherStatement.objects.filter(id=teacher_statement_id).exists():
        teacher_statement = TeacherStatement.objects.get(id=teacher_statement_id)
    else:
        return Response({"detail": "Teacher statement not found"}, status=404)

    teacher_statement.verdict = verdict.upper()
    teacher_statement.verdict_date = timezone.now()
    teacher_statement.save()

    return Response({"detail": "Success"})


# Filter API views


@api_view(http_method_names=["GET", "POST"])
@validate_payload(
    keys=[
        "high_schools",
        "faculties",
        "departments",
        "specializations",
        "study_years",
        "payment_types",
        "genders",
        "nationalities",
        "regions",
        "countries",
        "military_service",
    ]
)
def filter_api_view(request: HttpRequest):
    response = {
        "students": [
            {"name": "Jemi", "count": 0, "query": 0},
            {"name": "Oglan", "count": 0, "query": 1},
            {"name": "Gyz", "count": 0, "query": 2},
        ],
        "degrees": [
            {"name": "Bakalawr", "count": 0},
            {"name": "Hünärmen", "count": 0},
            {"name": "Aspirantura", "count": 0},
            {"name": "Magistratura", "count": 0},
            {"name": "Bakalawr tölegli", "count": 0},
            {"name": "Hünärmen tölegli", "count": 0},
            {"name": "Aspirantura tölegli", "count": 0},
            {"name": "Magistratura tölegli", "count": 0},
            {"name": "Bakalawr tölegsiz", "count": 0},
            {"name": "Hünärmen tölegsiz", "count": 0},
            {"name": "Aspirantura tölegsiz", "count": 0},
            {"name": "Magistratura tölegsiz", "count": 0},
        ],
        "high_schools": [
            {"id": high_school.id, "name": high_school.name}
            for high_school in HighSchool.objects.filter(active=True)
        ],
        "faculties": [
            {"id": faculty.id, "name": faculty.name}
            for faculty in Faculty.objects.filter(active=True)
        ],
        "departments": [
            {"id": department.id, "name": department.name}
            for department in Department.objects.filter(active=True)
        ],
        "specializations": [
            {"id": specialization.id, "name": specialization.name}
            for specialization in Specialization.objects.filter(active=True)
        ],
        "study_years": [
            {"id": 1, "name": "I kurs"},
            {"id": 2, "name": "II kurs"},
            {"id": 3, "name": "III kurs"},
            {"id": 4, "name": "IV kurs"},
            {"id": 5, "name": "V kurs"},
            {"id": 6, "name": "VI kurs"},
            {"id": 7, "name": "VII kurs"},
        ],
        "payment_types": [
            {"id": 1, "name": "Tölegli"},
            {"id": 2, "name": "Býudjet"},
        ],
        "genders": [
            {"id": 1, "name": "Oglan"},
            {"id": 2, "name": "Gyz"},
        ],
        "nationalities": [
            {"id": nationality.id, "name": nationality.name}
            for nationality in Nationality.objects.all()
        ],
        "countries": [
            {"id": country.id, "name": country.name}
            for country in Country.objects.all()
        ],
        "regions": [
            {"id": region.id, "name": region.name, "count": 0}
            for region in Region.objects.all()
        ],
    }
    if request.method == "POST":
        faculty_ids = [faculty["id"] for faculty in response["faculties"]]
        department_ids = [department["id"] for department in response["departments"]]
        specialization_ids = [
            specializiation["id"] for specializiation in response["specializations"]
        ]
        if len(request.data["high_schools"]) > 0:
            faculty_ids.clear()
            department_ids.clear()
            specialization_ids.clear()
            for high_school_id in request.data["high_schools"]:
                [
                    faculty_ids.append(faculty.id)
                    for faculty in Faculty.objects.filter(
                        id__in=[
                            high_school_faculty.faculty.id
                            for high_school_faculty in HighSchoolFaculty.objects.filter(
                                high_school__id=high_school_id
                            )
                        ],
                        active=True,
                    )
                ]
                [
                    department_ids.append(department.id)
                    for department in Department.objects.filter(
                        id__in=[
                            faculty_department.department.id
                            for faculty_department in FacultyDepartment.objects.filter(
                                high_school_faculty__high_school__id=high_school_id,
                            )
                        ],
                        active=True,
                    )
                ]
                [
                    specialization_ids.append(specialization.id)
                    for specialization in Specialization.objects.filter(
                        id__in=[
                            department_specialization.specialization.id
                            for department_specialization in DepartmentSpecialization.objects.filter(
                                faculty_department__high_school_faculty__high_school__id=high_school_id,
                            )
                        ],
                        active=True,
                    )
                ]
            faculty_ids = list(set(faculty_ids))
            department_ids = list(set(department_ids))
            specialization_ids = list(set(specialization_ids))

        if len(request.data["faculties"]) > 0:
            department_ids.clear()
            specialization_ids.clear()
            for faculty_id in request.data["faculties"]:
                [
                    department_ids.append(department.id)
                    for department in Department.objects.filter(
                        id__in=[
                            faculty_department.department.id
                            for faculty_department in FacultyDepartment.objects.filter(
                                high_school_faculty__faculty__id=faculty_id,
                            )
                        ],
                        active=True,
                    )
                ]
                [
                    specialization_ids.append(specialization.id)
                    for specialization in Specialization.objects.filter(
                        id__in=[
                            department_specialization.specialization.id
                            for department_specialization in DepartmentSpecialization.objects.filter(
                                faculty_department__high_school_faculty__faculty__id=faculty_id,
                            )
                        ],
                        active=True,
                    )
                ]
            department_ids = list(set(department_ids))
            specialization_ids = list(set(specialization_ids))
        if len(request.data["departments"]) > 0:
            specialization_ids.clear()
            for department_id in request.data["departments"]:
                [
                    specialization_ids.append(specialization.id)
                    for specialization in Specialization.objects.filter(
                        id__in=[
                            department_specialization.specialization.id
                            for department_specialization in DepartmentSpecialization.objects.filter(
                                faculty_department__department__id=department_id,
                            )
                        ],
                        active=True,
                    )
                ]
            specialization_ids = list(set(specialization_ids))

        response["faculties"] = [
            {"id": faculty.id, "name": faculty.name}
            for faculty in Faculty.objects.filter(id__in=faculty_ids)
        ]
        response["departments"] = [
            {"id": department.id, "name": department.name}
            for department in Department.objects.filter(id__in=department_ids)
        ]

        response["specializations"] = [
            {"id": specialization.id, "name": specialization.name}
            for specialization in Specialization.objects.filter(
                id__in=specialization_ids
            )
        ]
        filter_output = advanced_quantity_filter(request.data)
        response["students"] = filter_output["students"]
        response["regions"] = filter_output["regions"]
        response["degrees"] = filter_output["degrees"]

    return Response(response)


@api_view(http_method_names=["POST"])
@validate_payload(
    keys=[
        "high_schools",
        "faculties",
        "departments",
        "specializations",
        "study_years",
        "payment_types",
        "genders",
        "nationalities",
        "regions",
        "countries",
        "military_service",
    ]
)
def filtered_students_api_view(request: HttpRequest):
    print(request.GET)
    return Response(
        advanced_filter(
            request.data,
            list(request.GET.keys())[0],
            int(request.GET.get(list(request.GET.keys())[0])),
        )
    )
