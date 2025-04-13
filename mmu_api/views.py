from rest_framework.decorators import api_view
from rest_framework.request import HttpRequest
from rest_framework.response import Response

# Create your views here.


@api_view(http_method_names=["GET"])
def get_user_data(request: HttpRequest):
    if request.user.is_superuser:
        notifications = []
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
                "manager_of": "hello",
                "email": request.user.email,
                "is_superuser": request.user.is_superuser,
            }
        )


@api_view(http_method_names=["GET"])
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
    return Response({"detail": "Permission denied."})
