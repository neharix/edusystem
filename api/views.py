import io

import numpy as np
import openpyxl
import pandas as pd
from django.conf import settings
from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponse
from django.utils import timezone
from rest_framework.decorators import api_view
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.request import HttpRequest
from rest_framework.response import Response

from .decorators import validate_files, validate_post
from .models import (
    Classificator,
    Country,
    Degree,
    Department,
    Faculty,
    HighSchool,
    Nationality,
    Profile,
    Region,
    Specialization,
    Student,
)
from .serializers import (
    ClassificatorSerializer,
    DegreeSerializer,
    DepartmentSerializer,
    HighSchoolSerializer,
    SpecializationSerializer,
    StudentSerializer,
)
from .utils import create_example, validate_not_null_field

# Special API views


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


@api_view(http_method_names=["POST"])
@validate_post(keys=["high_school_id"])
@validate_files(keys=["excel"])
def import_excel_data(request: HttpRequest):
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
                f"Setir №{index + 2}: '{','.join(row_status[1])}' meýdançasy boş bolup bilmez"
            )
        else:
            full_name = row["F.A.Aa"]
            birth_date = row["Doglan senesi"].to_pydatetime()

            if row["Jynsy"] in ("Oglan", "Gyz"):
                gender = "M" if row["Jynsy"] == "Oglan" else "F"
            else:
                invalid_fields.append(
                    f"Setir №{index + 2}: 'Jynsy' meýdançasynda ýalňyşlyk goýberildi"
                )
                row_validation = False

            if Region.objects.filter(name=row["Welaýaty"]).exists():
                region = Region.objects.get(name=row["Welaýaty"])
            else:
                invalid_fields.append(
                    f"Setir №{index + 2}: 'Welaýaty' meýdançasynda ýalňyşlyk goýberildi"
                )
                row_validation = False

            if Nationality.objects.filter(name=row["Milleti"]).exists():
                nationality = Nationality.objects.get(name=row["Milleti"])
            else:
                invalid_fields.append(
                    f"Setir №{index + 2}: 'Milleti' meýdançasynda ýalňyşlyk goýberildi"
                )
                row_validation = False

            if Country.objects.filter(name=row["Ýurdy"]).exists():
                country = Country.objects.get(name=row["Ýurdy"])
            else:
                invalid_fields.append(
                    f"Setir №{index + 2}: 'Milleti' meýdançasynda ýalňyşlyk goýberildi"
                )
                row_validation = False

            if Faculty.objects.filter(name=row["Fakulteti"]).exists():
                faculty = Faculty.objects.get(name=row["Fakulteti"])
            else:
                invalid_fields.append(
                    f"Setir №{index + 2}: 'Fakulteti' meýdançasynda ýalňyşlyk goýberildi"
                )
                row_validation = False

            if Department.objects.filter(name=row["Kafedrasy"]):
                department = Department.objects.get(name=row["Kafedrasy"])
            else:
                invalid_fields.append(
                    f"Setir №{index + 2}: 'Kafedrasy' meýdançasynda ýalňyşlyk goýberildi"
                )
                row_validation = False

            if Specialization.objects.filter(name=row["Hünari"]):
                specialization = Specialization.objects.get(name=row["Hünari"])
            else:
                invalid_fields.append(
                    f"Setir №{index + 2}: 'Hünäri' meýdançasynda ýalňyşlyk goýberildi"
                )
                row_validation = False

            if type(row["Kursy"]) == int:
                course = row["Kursy"]
            else:
                invalid_fields.append(
                    f"Setir №{index + 2}: 'Kursy' meýdançasynda ýalňyşlyk goýberildi"
                )
                row_validation = False

            if row["Töleg görnüşi"] in ("Tölegli", "Býudjet"):
                payment_type = "P" if row["Töleg görnüşi"] == "Tölegli" else "B"
            else:
                invalid_fields.append(
                    f"Setir №{index + 2}: 'Töleg görnüşi' meýdançasynda ýalňyşlyk goýberildi"
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
                    f"Setir №{index + 2}: 'Maşgala ýagdaýy' meýdançasynda ýalňyşlyk goýberildi"
                )
                row_validation = False

            if type(row["Ýazgyda duran salgysy"]) == str:
                registered_place = row["Ýazgyda duran salgysy"]
            else:
                invalid_fields.append(
                    f"Setir №{index + 2}: 'Ýazgyda duran salgysy' meýdançasynda ýalňyşlyk goýberildi"
                )
                row_validation = False

            if (
                type(row["Öý, iş, mobil telefony"]) == str
                or type(row["Öý, iş, mobil telefony"]) == int
            ):
                phone_number = row["Öý, iş, mobil telefony"]
            else:
                invalid_fields.append(
                    f"Setir №{index + 2}: 'Öý, iş, mobil telefony' meýdançasynda ýalňyşlyk goýberildi"
                )
                row_validation = False

            if type(row["Pasport seriýasy, belgisi"]) == str:
                passport = row["Pasport seriýasy, belgisi"]
            else:
                invalid_fields.append(
                    f"Setir №{index + 2}: 'Pasport seriýasy, belgisi' meýdançasynda ýalňyşlyk goýberildi"
                )
                row_validation = False

            admission_date = row["Okuwa giren senesi"].to_pydatetime()

            if row_validation:
                student = Student.objects.create(
                    full_name=full_name,
                    gender=gender,
                    family_status=family_status,
                    payment_type=payment_type,
                    nationality=nationality,
                    country=country,
                    region=region,
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

    if len(invalid_fields) > 0:
        return Response(
            {
                "detail": "Success, but there are some mistakes",
                "mistakes": invalid_fields,
            }
        )
    return Response({"detail": "Success"})


@api_view(http_method_names=["GET"])
def root_dashboard_api_view(request: HttpRequest):
    if request.user.is_superuser or settings.DEV_STATUS:
        return Response(
            {
                "high_schools_count": HighSchool.objects.filter(active=True).count(),
                "faculties_count": Faculty.objects.filter(active=True).count(),
                "departments_count": Department.objects.filter(active=True).count(),
                "specializations_count": Specialization.objects.filter(
                    active=True
                ).count(),
                "nationalities_count": Nationality.objects.all().count(),
                "students_count": Student.objects.all().count(),
                "male_students_count": Student.objects.filter(gender="M").count(),
                "female_students_count": Student.objects.filter(gender="F").count(),
            }
        )
    else:
        return Response({"detail": "Permission denied."})


# High school API views


@api_view(http_method_names=["POST"])
@validate_post(keys=["name", "abbreviation", "username", "password"])
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


class DepartmentListCreateAPIView(ListCreateAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    lookup_field = "id"


class DepartmentRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    lookup_field = "id"


# Degree API views


class DegreeListCreateAPIView(ListCreateAPIView):
    queryset = Degree.objects.all()
    serializer_class = DegreeSerializer
    lookup_field = "id"


class DegreeRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Degree.objects.all()
    serializer_class = DegreeSerializer
    lookup_field = "id"


# Classificator API views


@api_view(http_method_names=["POST"])
@validate_post(keys=["name"])
def create_classificator_api_view(request: HttpRequest):
    classificator = Classificator.objects.create(name=request.data["name"])
    return Response({"detail": "Success", "id": classificator.id})


@api_view(http_method_names=["GET"])
def get_classificators_api_view(request: HttpRequest):
    classificator_serializer = ClassificatorSerializer(
        Classificator.objects.all(), many=True
    )
    return Response(classificator_serializer.data)


@api_view(http_method_names=["GET"])
def get_classificator_api_view(request: HttpRequest, classificator_id: int):
    if Classificator.objects.filter(id=classificator_id).exists():
        classificator = Classificator.objects.get(id=classificator_id)
    else:
        return Response({"detail": "Classificator doesn't exist"})
    classificator_serializer = ClassificatorSerializer(classificator)
    return Response(classificator_serializer.data)


# Specialization API views


@api_view(http_method_names=["POST"])
@validate_post(keys=["name", "abbreviation", "classificator", "degree"])
def create_specialization_api_view(request: HttpRequest):
    if Classificator.objects.filter(id=request.data["classificator"]).exists():
        classificator = Classificator.objects.get(id=request.data["classificator"])
    else:
        return Response({"detail": "Classificator doesn't exist"})
    if Degree.objects.filter(id=request.data["degree"]).exists():
        degree = Degree.objects.get(id=request.data["degree"])
    else:
        return Response({"detail": "Degree doesn't exist"})

    specialization = Specialization.objects.create(
        name=request.data["name"],
        abbreviation=request.data["abbreviation"],
        classificator=classificator,
        degree=degree,
    )
    return Response({"detail": "Success", "id": specialization.id})


@api_view(http_method_names=["GET"])
def get_specializations_api_view(request: HttpRequest):
    specialization_serializer = SpecializationSerializer(
        Specialization.objects.filter(active=True), many=True
    )
    return Response(specialization_serializer.data)


@api_view(http_method_names=["GET"])
def get_specialization_api_view(request: HttpRequest, specialization_id: int):
    if Specialization.objects.filter(id=specialization_id).exists():
        specialization = Specialization.objects.get(id=specialization_id)
    else:
        return Response({"detail": "Specialization doesn't exist"})
    specialization_serializer = SpecializationSerializer(specialization)
    return Response(specialization_serializer.data)


# Student API views


@api_view(http_method_names=["GET"])
def get_students_api_view(request: HttpRequest):
    student_serializer = StudentSerializer(Student.objects.all(), many=True)
    return Response(student_serializer.data)


@api_view(http_method_names=["GET"])
def get_student_api_view(request: HttpRequest, student_id: int):
    if Student.objects.filter(id=student_id).exists():
        student = Student.objects.get(id=student_id)
    else:
        return Response({"detail": "Student doesn't exist"})
    student_serializer = StudentSerializer(student)
    return Response(student_serializer.data)


# Nationalization API views


@api_view(http_method_names=["POST"])
@validate_post(keys=["name", "abbreviation", "classificator", "degree"])
def create_specialization_api_view(request: HttpRequest):
    if Classificator.objects.filter(id=request.data["classificator"]).exists():
        classificator = Classificator.objects.get(id=request.data["classificator"])
    else:
        return Response({"detail": "Classificator doesn't exist"})
    if Degree.objects.filter(id=request.data["degree"]).exists():
        degree = Degree.objects.get(id=request.data["degree"])
    else:
        return Response({"detail": "Degree doesn't exist"})

    specialization = Specialization.objects.create(
        name=request.data["name"],
        abbreviation=request.data["abbreviation"],
        classificator=classificator,
        degree=degree,
    )
    return Response({"detail": "Success", "id": specialization.id})


@api_view(http_method_names=["GET"])
def get_specializations_api_view(request: HttpRequest):
    specialization_serializer = SpecializationSerializer(
        Specialization.objects.filter(active=True), many=True
    )
    return Response(specialization_serializer.data)


@api_view(http_method_names=["GET"])
def get_specialization_api_view(request: HttpRequest, specialization_id: int):
    if Specialization.objects.filter(id=specialization_id).exists():
        specialization = Specialization.objects.get(id=specialization_id)
    else:
        return Response({"detail": "Specialization doesn't exist"})
    specialization_serializer = SpecializationSerializer(specialization)
    return Response(specialization_serializer.data)
