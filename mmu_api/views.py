import base64
import io
import json
import mimetypes
import os

import qrcode
from django.conf import settings
from django.contrib.auth.models import User
from django.http import HttpResponse, StreamingHttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.templatetags.static import static
from django.utils import timezone
from django.views.decorators.cache import cache_page
from rest_framework.decorators import api_view
from rest_framework.request import HttpRequest
from rest_framework.response import Response
from weasyprint import HTML

from main.decorators import validate_files, validate_payload
from main.models import Profile
from main.paginators import ResponsivePageSizePagination

# from main.serializers import CountrySerializer, NationalitySerializer, RegionSerializer
from main.utils import file_iterator, is_valid_files, is_valid_payload

from .decorators import check_service_status, login_required
from .models import (
    Achievement,
    Certificate,
    Country,
    Course,
    EducationCenter,
    File,
    Nationality,
    Region,
    Specialization,
    Staff,
    Student,
)
from .serializers import (
    AboutEducationCenterSerializer,
    AchievementAdditionalSerializer,
    AchievementSerializer,
    CertificateSerializer,
    CountrySerializer,
    CourseSerializer,
    EducationCenterAdditionalSerializer,
    EducationCenterSerializer,
    FileSerializer,
    NationalitySerializer,
    ProfileAdditionalSerializer,
    RegionSerializer,
    SpecializationAdditionalSerializer,
    SpecializationSerializer,
    StaffSerializer,
    StudentAdditionalSerializer,
    StudentSerializer,
)
from .utils import action_logger, is_admin, xlsx_exporter, xlsx_importer

# Create your views here.


@api_view(http_method_names=["POST"])
@validate_payload(["username"])
def try_otp_api_view(request: HttpRequest):
    if Profile.objects.filter(user__username=request.data["username"]).exists():
        profile = Profile.objects.get(user__username=request.data["username"])
        profile.generate_otp()
        if profile.user.email:
            # TODO add smtp service
            email_splitted = profile.user.email.split("@")
            email_useful_part = email_splitted[0]
            if len(email_useful_part) >= 3:
                email = (
                    "".join(
                        [
                            email_useful_part[char_id] if char_id < 3 else "*"
                            for char_id in range(len(email_useful_part))
                        ]
                    )
                    + "@"
                    + "".join(
                        [
                            email_splitted[part_id] if part_id != 0 else ""
                            for part_id in range(len(email_splitted))
                        ]
                    )
                )
            else:
                email = (
                    email_useful_part[0]
                    + email_useful_part[1]
                    + "**"
                    + "@"
                    + "".join(
                        [
                            email_splitted[part_id] if part_id != 0 else ""
                            for part_id in range(len(email_splitted))
                        ]
                    )
                )

            return Response(
                {
                    "email": email,
                    "username": profile.user.username,
                    "temp_key": profile.temp_key,
                }
            )
        else:
            return Response(
                {"detail": "This account have not available email"}, status=400
            )
    else:
        return Response({"detail": "User not found"}, status=404)


@api_view(http_method_names=["POST"])
@validate_payload(["user", "otp"])
def check_otp_api_view(request: HttpRequest):
    if Profile.objects.filter(user__username=request.data["user"]).exists():
        profile = Profile.objects.get(user__username=request.data["user"])
        if request.data["otp"] == profile.otp:
            return Response({"is_successfully": True, "temp_key": profile.temp_key})
        else:
            return Response({"is_successfully": False})
    else:
        return Response({"detail": "User not found"}, status=404)


@api_view(http_method_names=["POST"])
@validate_payload(["username", "password", "secure_key"])
def change_password_api_view(request: HttpRequest):
    if Profile.objects.filter(
        user__username=request.data["username"], temp_key=request.data["secure_key"]
    ).exists():
        profile = Profile.objects.get(user__username=request.data["username"])
        user = profile.user
        user.set_password(request.data["password"])
        user.save()
        profile.password = request.data["password"]
        profile.save()
        return Response({"detail": "Success"})
    else:
        return Response({"detail": "User not found"}, status=404)


@api_view(http_method_names=["GET"])
@login_required()
def get_user_data(request: HttpRequest):
    if request.user.is_superuser:
        with open(
            os.path.join(settings.BASE_DIR / "mmu_api/config.json"),
            "r",
            encoding="utf-8",
        ) as cfg_file:
            service_status = json.loads(cfg_file.read())["is_enabled"]

        notifications = []
        return Response(
            {
                "id": request.user.id,
                "is_superuser": request.user.is_superuser,
                "notifications": notifications,
                "is_service_enabled": service_status,
            }
        )
    else:
        return Response(
            {
                "id": request.user.id,
                "manager_of": "hello",
                "is_superuser": request.user.is_superuser,
            }
        )


@api_view(http_method_names=["GET"])
@login_required()
@check_service_status()
@cache_page(60 * 2)
def dashboard_api_view(request: HttpRequest):
    if is_admin(request):
        return Response(
            {
                "education_centers_count": 1,
                "nationalities_count": 30,
                "students_count": 70,
                "male_students_count": 30,
                "female_students_count": 40,
                "admissions": [
                    {
                        "year": 2022,
                        "male_students_count": 30,
                        "female_students_count": 40,
                    }
                ],
            }
        )
    else:
        # high_school = HighSchool.objects.get(manager__user=request.user)
        return Response(
            {
                # FIXME
                "nationalities_count": 30,
                "students_count": 70,
                "male_students_count": 30,
                "female_students_count": 40,
                "admissions": [
                    {
                        "year": 2022,
                        "male_students_count": 30,
                        "female_students_count": 40,
                    }
                ],
            }
        )


@api_view(http_method_names=["GET"])
@login_required(is_admin=True)
def toggle_service_status(request: HttpRequest):
    with open(
        os.path.join(settings.BASE_DIR / "mmu_api/config.json"), "r", encoding="utf-8"
    ) as cfg_file:
        cfg = json.loads(cfg_file.read())
    if cfg["is_enabled"]:
        cfg["is_enabled"] = False
        action_logger(request, "")
    else:
        cfg["is_enabled"] = True

    with open(
        os.path.join(settings.BASE_DIR / "mmu_api/config.json"), "w", encoding="utf-8"
    ) as cfg_file:
        cfg_file.write(json.dumps(cfg))
    return Response({"detail": "Success", "is_enabled": cfg["is_enabled"]})


@api_view(http_method_names=["POST"])
@login_required(is_admin=True)
@validate_payload(["model", "identificators"])
@check_service_status()
def export_data(request: HttpRequest):
    workbook = xlsx_exporter(request.data["model"], request.data["identificators"])

    with io.BytesIO() as buffer:
        workbook.save(buffer)
        content = buffer.getvalue()

    response = HttpResponse(
        content=content,
        content_type="application/xlsx",
    )
    filename = f"{request.data['model']}-{timezone.now().strftime('%d-%m-%Y')}.xlsx"
    response["Content-Disposition"] = f'attachment; filename="' + filename + '"'
    return response


@api_view(http_method_names=["POST"])
@login_required(is_admin=True)
@validate_payload(["model", "identificators"])
@check_service_status()
def delete_data(request: HttpRequest):
    metas = []
    match request.data["model"]:
        case "profile":
            data = Profile.objects.filter(id__in=request.data["identificators"])
            user_ids = [item.user.id for item in data]
            users = User.objects.filter(id__in=user_ids)
            metas.append(users)
        case "education-center":
            data = EducationCenter.objects.filter(id__in=request.data["identificators"])
        case "achievement":
            data = Achievement.objects.filter(id__in=request.data["identificators"])
        case "specialization":
            data = Specialization.objects.filter(id__in=request.data["identificators"])

    data.delete()

    while len(metas) > 0:
        metas[len(metas) - 1].delete()

    return Response({"detail": "Success"})


@api_view(http_method_names=["POST"])
@login_required()
@validate_payload(["model"])
@validate_files(["excel"])
@check_service_status()
def import_data(request: HttpRequest):
    xlsx_importer(request.data["model"], request.FILES["excel"])
    return Response({"detail": "Success"})


@api_view(http_method_names=["GET"])
@login_required()
@check_service_status()
def profile_list_view(request: HttpRequest):
    page_size = int(request.GET.get("page_size", 10))
    order = "-" if request.GET.get("order", "asc") == "desc" else ""
    order_key = request.GET.get("column", "username")
    search = request.GET.get("search", False)

    match order_key:
        case "username":
            order_key = "user__username"
        case "email":
            order_key = "user__email"
        case "user_id":
            order_key = "user__id"

    order_by = order + order_key

    if is_admin(request):
        profiles = (
            Profile.objects.filter(
                allowed_service="mmu", user__username__contains=search
            ).select_related("user")
            if search
            else Profile.objects.filter(allowed_service="mmu").select_related("user")
        ).order_by(order_by)
        paginator = ResponsivePageSizePagination()
        paginator.page_size = page_size
        paginated_result = paginator.paginate_queryset(profiles, request)
        serializer = ProfileAdditionalSerializer(paginated_result, many=True)
        return paginator.get_paginated_response(
            {"data": serializer.data, "total_pages": paginator.page.paginator.num_pages}
        )
    else:
        # high_school = HighSchool.objects.get(manager__user=request.user)
        return Response(
            {
                # FIXME
                "nationalities_count": 30,
                "students_count": 70,
                "male_students_count": 30,
                "female_students_count": 40,
                "admissions": [
                    {
                        "year": 2022,
                        "male_students_count": 30,
                        "female_students_count": 40,
                    }
                ],
            }
        )


# Education center API views


@api_view(http_method_names=["GET", "POST"])
@login_required(is_admin=True)
def education_center_list_create_view(request: HttpRequest):
    match request.method:
        case "GET":
            page_size = int(request.GET.get("page_size", 10))
            order = "-" if request.GET.get("order", "asc") == "desc" else ""
            order_key = request.GET.get("column", "name")
            search = request.GET.get("search", False)

            order_by = order + order_key

            filters = {}
            if request.GET.get("region", False):
                filters["region__id__exact"] = request.GET["region"]
            if request.GET.get("country", False):
                filters["country__id__exact"] = request.GET["country"]

            education_centers = (
                EducationCenter.objects.filter(
                    is_active=True, name__contains=search, **filters
                )
                if search
                else EducationCenter.objects.filter(is_active=True, **filters)
            ).order_by(order_by)

            paginator = ResponsivePageSizePagination()
            paginator.page_size = page_size
            paginated_result = paginator.paginate_queryset(education_centers, request)
            serializer = EducationCenterAdditionalSerializer(
                paginated_result, many=True
            )
            return paginator.get_paginated_response(
                {
                    "data": serializer.data,
                    "total_pages": paginator.page.paginator.num_pages,
                }
            )
        case "POST":
            if is_admin(request):
                if is_valid_payload(
                    request,
                    [
                        "name",
                        "phone_number",
                        "address",
                        "region",
                        "country",
                        "buildings_count",
                        "capacity",
                        "rooms_count",
                        "books_count",
                        "lng",
                        "lat",
                    ],
                ):
                    if not EducationCenter.objects.filter(
                        name=request.data["name"].strip()
                    ).exists():
                        try:
                            region = Region.objects.get(id=request.data["region"])
                        except:
                            return Response({"detail": "Region not found"}, status=404)

                        try:
                            country = Country.objects.get(id=request.data["country"])
                        except:
                            return Response({"detail": "Country not found"}, status=404)

                        EducationCenter.objects.create(
                            name=request.data["name"].strip(),
                            phone_number=request.data["phone_number"],
                            address=request.data["address"],
                            region=region,
                            country=country,
                            buildings_count=request.data["buildings_count"],
                            rooms_count=request.data["rooms_count"],
                            capacity=request.data["capacity"],
                            books_count=request.data["books_count"],
                        )
                        return Response({"detail": "Success"})
                    else:
                        return Response(
                            {"detail": "Education center already exist"}, status=400
                        )
                else:
                    return Response({"detail": "Payload invalid"}, status=400)
            else:
                return Response({"detail": "Permission denied"}, status=403)


@api_view(http_method_names=["GET", "PUT", "PATCH", "DELETE"])
@login_required()
def education_center_retrieve_update_delete_view(
    request: HttpRequest, education_center_id: int
):
    if EducationCenter.objects.filter(id=education_center_id, is_active=True).exists():
        education_center = EducationCenter.objects.get(id=education_center_id)
    else:
        return Response({"detail": "Education center not found"}, status=404)

    match request.method:
        case "GET":
            return Response(EducationCenterSerializer(education_center).data)
        case "PUT":
            if is_valid_payload(
                request,
                [
                    "name",
                    "phone_number",
                    "address",
                    "region",
                    "country",
                    "buildings_count",
                    "capacity",
                    "rooms_count",
                    "books_count",
                    "lng",
                    "lat",
                ],
            ):
                try:
                    region = Region.objects.get(id=request.data["region"])
                except:
                    return Response({"detail": "Region not found"}, status=404)

                try:
                    country = Country.objects.get(id=request.data["country"])
                except:
                    return Response({"detail": "Country not found"}, status=404)

                education_center.name = request.data["name"]
                education_center.phone_number = request.data["phone_number"]
                education_center.address = request.data["address"]
                education_center.region = region
                education_center.country = country
                education_center.buildings_count = request.data["buildings_count"]
                education_center.books_count = request.data["books_count"]
                education_center.rooms_count = request.data["rooms_count"]
                education_center.capacity = request.data["capacity"]
                education_center.lng = request.data["lng"]
                education_center.lat = request.data["lat"]
                education_center.save()
                return Response({"detail": "Updated", "id": education_center.id})
            else:
                return Response({"detail": "Payload invalid"}, status=400)

        case "DELETE":
            idf = education_center.id
            education_center.delete()
            return Response({"detail": "Deactivated", "id": idf})


@api_view(http_method_names=["GET"])
@login_required(is_admin=True)
def about_education_center(request: HttpRequest, education_center_id: int):
    if EducationCenter.objects.filter(id=education_center_id, is_active=True).exists():
        education_center = EducationCenter.objects.get(id=education_center_id)
    else:
        return Response({"detail": "Education center not found"}, status=404)
    return Response(AboutEducationCenterSerializer(education_center).data)


@api_view(http_method_names=["GET"])
@login_required(is_admin=True)
def get_education_center_files(request: HttpRequest, education_center_id: int):
    page_size = int(request.GET.get("page_size", 10))
    order = "-" if request.GET.get("order", "asc") == "desc" else ""
    order_key = request.GET.get("column", "name")

    match order_key:
        case "uploader":
            order_key = "uploader__user__username"

    search = request.GET.get("search", False)

    order_by = order + order_key

    if EducationCenter.objects.filter(id=education_center_id, is_active=True).exists():
        education_center = EducationCenter.objects.get(id=education_center_id)
    else:
        return Response({"detail": "Education center not found"}, status=404)

    files = (
        (
            File.objects.filter(to_storage=education_center, name__contains=search)
            if search
            else File.objects.filter(to_storage=education_center)
        )
        .select_related("uploader", "uploader__user", "to", "to__user", "to_storage")
        .order_by(order_by)
    )

    paginator = ResponsivePageSizePagination()
    paginator.page_size = page_size
    paginated_result = paginator.paginate_queryset(files, request)
    serializer = FileSerializer(paginated_result, many=True)

    return paginator.get_paginated_response(
        {"data": serializer.data, "total_pages": paginator.page.paginator.num_pages}
    )


@api_view(http_method_names=["GET"])
@login_required(is_admin=True)
def get_education_center_staff(request: HttpRequest, education_center_id: int):
    page_size = int(request.GET.get("page_size", 10))
    order = "-" if request.GET.get("order", "asc") == "desc" else ""
    order_key = request.GET.get("column", "full_name")

    match order_key:
        case "region":
            order_key = "region__name"
        case "country":
            order_key = "country__name"

    order_by = order + order_key

    search = request.GET.get("search", False)

    if EducationCenter.objects.filter(id=education_center_id, is_active=True).exists():
        education_center = EducationCenter.objects.get(id=education_center_id)
    else:
        return Response({"detail": "Education center not found"}, status=404)

    staff = education_center.staff.filter(is_active=True)
    if search:
        staff = staff.filter(full_name__contains=search).order_by(order_by)
    else:
        staff = staff.order_by(order_by)

    paginator = ResponsivePageSizePagination()
    paginator.page_size = page_size
    paginated_result = paginator.paginate_queryset(staff, request)
    serializer = StaffSerializer(paginated_result, many=True)

    return paginator.get_paginated_response(
        {"data": serializer.data, "total_pages": paginator.page.paginator.num_pages}
    )


# Region API views
@api_view(http_method_names=["GET"])
@login_required()
@check_service_status()
def region_list_view(request: HttpRequest):
    if is_admin(request):
        response_as = request.GET.get("as", "all")
        match response_as:
            case "all":
                return Response(RegionSerializer(Region.objects.all(), many=True).data)
            case "page":
                return Response({"detail": "FIXME"})
    else:
        return Response({"detail": "FIXME"})


# Nationality API views
@api_view(http_method_names=["GET"])
@login_required()
@check_service_status()
def nationality_list_view(request: HttpRequest):
    if is_admin(request):
        return Response(
            NationalitySerializer(Nationality.objects.all(), many=True).data
        )
    else:
        return Response({"detail": "FIXME"})


# Country API views
@api_view(http_method_names=["GET"])
@login_required()
@check_service_status()
def country_list_view(request: HttpRequest):
    if is_admin(request):
        response_as = request.GET.get("as", "all")
        match response_as:
            case "all":
                return Response(
                    CountrySerializer(Country.objects.all(), many=True).data
                )
            case "page":
                return Response({"detail": "FIXME"})
    else:
        return Response({"detail": "FIXME"})


# File API views


@api_view(http_method_names=["GET"])
@login_required()
def download_file(request: HttpRequest, file_id: str):

    if File.objects.filter(id=file_id).exists():
        file = File.objects.get(id=file_id)
    else:
        return Response({"detail": "File not found"}, status=404)

    file_path = file.content.path
    file_name = file.content.name.split("/")[-1]

    try:
        file_size = os.path.getsize(file_path)
    except FileNotFoundError as e:
        return Response({"detail": "File not found at server storage"}, status=404)

    response = StreamingHttpResponse(
        file_iterator(file_path), content_type=mimetypes.guess_type(file_name)
    )
    response["Content-Disposition"] = f"attachment; filename={file_name}"
    response["Content-Length"] = file_size
    return response


@api_view(http_method_names=["GET", "POST"])
@login_required()
@check_service_status()
def file_list_create_view(request: HttpRequest):
    match request.method:
        case _:
            pass
        # FIXME
        # case "GET":
        #     return Response(FileSerializer(File.objects.all(), many=True).data)
        # case "POST":
        #     if is_valid_payload([]) and is_valid_files():
        #         pass


@api_view(http_method_names=["GET", "DELETE", "PUT", "PATCH"])
@login_required()
@check_service_status()
def file_retrieve_delete_view(request: HttpRequest, file_id):
    if File.objects.filter(id=file_id).exists():
        file = File.objects.get(id=file_id)
    else:
        return Response({"detail": "File not found"}, status=404)
    match request.method:
        case "GET":
            return Response(FileSerializer(file).data)
        case "DELETE":
            os.remove(file.content.path)
            file.delete()
            return Response({"detail": "Success", "id": file_id})


# Achievement API views


@api_view(http_method_names=["GET", "POST"])
@login_required(is_admin=True)
def achievement_list_create_view(request: HttpRequest):
    match request.method:
        case "GET":
            page_size = int(request.GET.get("page_size", 10))
            order = "-" if request.GET.get("order", "asc") == "desc" else ""
            order_key = request.GET.get("column", "name")
            search = request.GET.get("search", False)

            order_by = order + order_key

            achievements = (
                Achievement.objects.filter(name__contains=search)
                if search
                else Achievement.objects.all()
            ).order_by(order_by)

            paginator = ResponsivePageSizePagination()
            paginator.page_size = page_size
            paginated_result = paginator.paginate_queryset(achievements, request)
            serializer = AchievementAdditionalSerializer(paginated_result, many=True)
            return paginator.get_paginated_response(
                {
                    "data": serializer.data,
                    "total_pages": paginator.page.paginator.num_pages,
                }
            )
        case "POST":
            if is_admin(request):
                if is_valid_payload(request, ["name"]):
                    if not Achievement.objects.filter(
                        name=request.data["name"].strip()
                    ).exists():
                        Achievement.objects.create(name=request.data["name"].strip())
                        return Response({"detail": "Success"})
                    else:
                        return Response(
                            {"detail": "Achievement already exist"}, status=400
                        )
                else:
                    return Response({"detail": "Payload invalid"}, status=400)
            else:
                return Response({"detail": "Permission denied"}, status=403)


@api_view(http_method_names=["GET", "PUT", "PATCH", "DELETE"])
@login_required()
def achievement_retrieve_update_delete_view(request: HttpRequest, achievement_id: int):
    if Achievement.objects.filter(id=achievement_id).exists():
        achievement = Achievement.objects.get(id=achievement_id)
    else:
        return Response({"detail": "Achievement not found"}, status=404)

    match request.method:
        case "GET":
            return Response(AchievementSerializer(achievement).data)
        case "PUT":
            if is_valid_payload(request, ["name"]):
                achievement.name = request.data["name"].strip()
                achievement.save()
                return Response({"detail": "Updated", "id": achievement.id})
            else:
                return Response({"detail": "Payload invalid"}, status=400)

        case "DELETE":
            idf = achievement.id
            achievement.delete()
            return Response({"detail": "Deactivated", "id": idf})


# Staff API views

# @api_view(http_method_names=["GET", "POST"])
# @login_required()
# @check_service_status()
# def staff_list_create_view(request: HttpRequest):


# Specialization API views


@api_view(http_method_names=["GET", "POST"])
@login_required(is_admin=True)
def specialization_list_create_view(request: HttpRequest):
    match request.method:
        case "GET":
            page_size = int(request.GET.get("page_size", 10))
            order = "-" if request.GET.get("order", "asc") == "desc" else ""
            order_key = request.GET.get("column", "name")
            search = request.GET.get("search", False)

            order_by = order + order_key

            specializations = (
                Specialization.objects.filter(name__contains=search)
                if search
                else Specialization.objects.all()
            ).order_by(order_by)

            paginator = ResponsivePageSizePagination()
            paginator.page_size = page_size
            paginated_result = paginator.paginate_queryset(specializations, request)
            serializer = SpecializationAdditionalSerializer(paginated_result, many=True)
            return paginator.get_paginated_response(
                {
                    "data": serializer.data,
                    "total_pages": paginator.page.paginator.num_pages,
                }
            )
        case "POST":
            if is_admin(request):
                if is_valid_payload(request, ["name"]):
                    if not Specialization.objects.filter(
                        name=request.data["name"].strip()
                    ).exists():
                        Specialization.objects.create(name=request.data["name"].strip())
                        return Response({"detail": "Success"})
                    else:
                        return Response(
                            {"detail": "Specialization already exist"}, status=400
                        )
                else:
                    return Response({"detail": "Payload invalid"}, status=400)
            else:
                return Response({"detail": "Permission denied"}, status=403)


@api_view(http_method_names=["GET", "PUT", "PATCH", "DELETE"])
@login_required()
def specialization_retrieve_update_delete_view(
    request: HttpRequest, specialization_id: int
):
    if Specialization.objects.filter(id=specialization_id).exists():
        specialization = Specialization.objects.get(id=specialization_id)
    else:
        return Response({"detail": "Specialization not found"}, status=404)

    match request.method:
        case "GET":
            return Response(SpecializationSerializer(specialization).data)
        case "PUT":
            if is_valid_payload(request, ["name"]):
                specialization.name = request.data["name"].strip()
                specialization.save()
                return Response({"detail": "Updated", "id": specialization.id})
            else:
                return Response({"detail": "Payload invalid"}, status=400)

        case "DELETE":
            idf = specialization.id
            specialization.delete()
            return Response({"detail": "Deactivated", "id": idf})


# Student API views


@api_view(http_method_names=["GET", "POST"])
@login_required(is_admin=True)
def student_list_create_view(request: HttpRequest):
    match request.method:
        case "GET":
            page_size = int(request.GET.get("page_size", 10))
            order = "-" if request.GET.get("order", "asc") == "desc" else ""
            order_key = request.GET.get("column", "full_name")
            search = request.GET.get("search", False)

            order_by = order + order_key

            filters = {}
            if request.GET.get("region", False):
                filters["region__id__exact"] = request.GET["region"]
            if request.GET.get("country", False):
                filters["country__id__exact"] = request.GET["country"]

            students = (
                Student.objects.filter(name__contains=search, **filters)
                if search
                else Student.objects.filter(**filters)
            ).order_by(order_by)

            paginator = ResponsivePageSizePagination()
            paginator.page_size = page_size
            paginated_result = paginator.paginate_queryset(students, request)
            serializer = StudentAdditionalSerializer(paginated_result, many=True)
            return paginator.get_paginated_response(
                {
                    "data": serializer.data,
                    "total_pages": paginator.page.paginator.num_pages,
                }
            )
        case "POST":
            if is_admin(request):
                if is_valid_payload(
                    request,
                    [
                        "name",
                        "phone_number",
                        "address",
                        "region",
                        "country",
                        "buildings_count",
                        "capacity",
                        "rooms_count",
                        "books_count",
                        "lng",
                        "lat",
                    ],
                ):
                    if not EducationCenter.objects.filter(
                        name=request.data["name"].strip()
                    ).exists():
                        try:
                            region = Region.objects.get(id=request.data["region"])
                        except:
                            return Response({"detail": "Region not found"}, status=404)

                        try:
                            country = Country.objects.get(id=request.data["country"])
                        except:
                            return Response({"detail": "Country not found"}, status=404)

                        EducationCenter.objects.create(
                            name=request.data["name"].strip(),
                            phone_number=request.data["phone_number"],
                            address=request.data["address"],
                            region=region,
                            country=country,
                            buildings_count=request.data["buildings_count"],
                            rooms_count=request.data["rooms_count"],
                            capacity=request.data["capacity"],
                            books_count=request.data["books_count"],
                        )
                        return Response({"detail": "Success"})
                    else:
                        return Response(
                            {"detail": "Education center already exist"}, status=400
                        )
                else:
                    return Response({"detail": "Payload invalid"}, status=400)
            else:
                return Response({"detail": "Permission denied"}, status=403)


@api_view(http_method_names=["GET", "PUT", "PATCH", "DELETE"])
@login_required()
def student_retrieve_update_delete_view(request: HttpRequest, student_id: int):
    if Student.objects.filter(id=student_id).exists():
        student = Student.objects.get(id=student_id)
    else:
        return Response({"detail": "Student not found"}, status=404)

    match request.method:
        case "GET":
            return Response(StudentSerializer(student).data)
        case "PUT":
            if is_valid_payload(
                request,
                [
                    "name",
                    "phone_number",
                    "address",
                    "region",
                    "country",
                    "buildings_count",
                    "capacity",
                    "rooms_count",
                    "books_count",
                    "lng",
                    "lat",
                ],
            ):
                # try:
                #     region = Region.objects.get(id=request.data["region"])
                # except:
                #     return Response({"detail": "Region not found"}, status=404)

                # try:
                #     country = Country.objects.get(id=request.data["country"])
                # except:
                #     return Response({"detail": "Country not found"}, status=404)

                # education_center.save()
                pass
                return Response({"detail": "Updated", "id": student.id})
            else:
                return Response({"detail": "Payload invalid"}, status=400)

        case "DELETE":
            idf = student.id
            student.delete()
            return Response({"detail": "Deactivated", "id": idf})


@api_view(http_method_names=["GET"])
@login_required(is_admin=True)
def get_student_courses(request: HttpRequest, student_id: int):
    if Student.objects.filter(id=student_id).exists():
        student = Student.objects.get(id=student_id)
    else:
        return Response({"detail": "Student not found"}, status=404)
    courses = Course.objects.filter(students__id=student.id)

    return Response(CourseSerializer(courses, many=True).data)


@api_view(http_method_names=["GET"])
@login_required(is_admin=True)
def get_student_certificates(request: HttpRequest, student_id: int):
    if Student.objects.filter(id=student_id).exists():
        student = Student.objects.get(id=student_id)
    else:
        return Response({"detail": "Student not found"}, status=404)
    certificates = Certificate.objects.filter(student=student)
    return Response(CertificateSerializer(certificates, many=True).data)


# def certificate_view(
#     request,
#     certificate_id: int,
# ):
#     if Certificate.objects.filter(id=certificate_id).exists():
#         certificate = Certificate.objects.get(id=certificate_id)

#     qr_data = request.build_absolute_uri(f"/certificates/{certificate.id}/")
#     qr_buffer = io.BytesIO()
#     qr_img = qrcode.make(qr_data)
#     qr_img.save(qr_buffer, format="PNG")
#     qr_base64 = base64.b64encode(qr_buffer.getvalue()).decode("utf-8")

#     # match request.headers["Accept-Language"]:
#     #     case "ru":
#     #         header = "Министерство Образования Туркменистана"
#     #         # desc = f"{}"

#     return render(
#         request,
#         "mmu_api/certificate.html",
#         {"qr_code_base64": qr_base64, "certificate": certificate},
#     )


def certificate_view(
    request,
    certificate_id: int,
):
    if Certificate.objects.filter(id=certificate_id).exists():
        certificate = Certificate.objects.get(id=certificate_id)

    qr_data = request.build_absolute_uri(f"/certificates/{certificate.id}/")
    qr_buffer = io.BytesIO()
    qr_img = qrcode.make(qr_data)
    qr_img.save(qr_buffer, format="PNG")
    qr_base64 = base64.b64encode(qr_buffer.getvalue()).decode("utf-8")

    data = {"qr_code_base64": qr_base64, "certificate": certificate}

    html_string = render_to_string(
        "mmu_api/certificate.html",
        data,
    )

    # Генерация PDF
    pdf_file = HTML(
        string=html_string, base_url=request.build_absolute_uri()
    ).write_pdf()

    # Ответ
    response = HttpResponse(pdf_file, content_type="application/pdf")
    response["Content-Disposition"] = 'inline; filename="certificate.pdf"'
    return response
