from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import HttpRequest
from rest_framework.response import Response
from silk.profiling.profiler import silk_profile

from api.models import Profile
from main.decorators import login_required, validate_payload


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
        notifications = []
        return Response(
            {
                "id": request.user.id,
                "is_superuser": request.user.is_superuser,
                "notifications": notifications,
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
@silk_profile(name="MMU Dashboard Profiler")
def dashboard_api_view(request: HttpRequest):
    if request.user.is_superuser:
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
    elif request.user.is_authenticated:
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
