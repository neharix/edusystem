import datetime

import pytz
from django.contrib.auth.models import User
from rest_framework import serializers

from .models import (
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


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email"]


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Profile
        fields = "__all__"


class FacultySerializer(serializers.ModelSerializer):
    class Meta:
        model = Faculty
        fields = "__all__"


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = "__all__"


class SpecializationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialization
        fields = "__all__"


class HighSchoolSerializer(serializers.ModelSerializer):
    manager = ProfileSerializer()
    # faculties = FacultySerializer(many=True)
    # departments = DepartmentSerializer(many=True)
    # specializations = SpecializationSerializer(many=True)

    class Meta:
        model = HighSchool
        fields = "__all__"


class DegreeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Degree
        fields = "__all__"


class ClassificatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classificator
        fields = "__all__"


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = "__all__"


class StudentAdditionalSerializer(serializers.ModelSerializer):
    high_school = HighSchoolSerializer()

    class Meta:
        model = Student
        fields = ["id", "full_name", "high_school", "study_year"]


class GraduateAdditionalSerializer(serializers.ModelSerializer):
    high_school = HighSchoolSerializer()
    study_period = serializers.SerializerMethodField()

    def get_study_period(self, instance):
        admission_year = instance.admission_date.year
        return f"{admission_year}-{admission_year + instance.specialization.specialization.degree.duration}"

    class Meta:
        model = Student
        fields = ["id", "full_name", "high_school", "study_period"]


class NationalitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Nationality
        fields = "__all__"


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = "__all__"


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = "__all__"


class ExpulsionReasonSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpulsionReason
        fields = "__all__"


class ExpulsionRequestSerializer(serializers.ModelSerializer):
    # request_type = serializers.SerializerMethodField()

    # def get_request_type(self, instance):
    #     return "expulsion"

    class Meta:
        model = ExpulsionRequest
        fields = [
            "sender",
            "reason",
            "student",
            "detail",
            "request_date",
            "verdict_date",
            "verdict",
            # "request_type",
        ]


class ReinstateRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReinstateRequest
        fields = [
            "sender",
            "student",
            "detail",
            "request_date",
            "verdict_date",
            "verdict",
        ]


# Student Info Serializers


class HighSchoolInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = HighSchool
        fields = ["name"]


class SpecializationInfoSerializer(serializers.ModelSerializer):
    degree = DegreeSerializer()

    class Meta:
        model = Specialization
        fields = "__all__"


class HighSchoolFacultyInfoSerializer(serializers.ModelSerializer):
    faculty = FacultySerializer()

    class Meta:
        model = HighSchoolFaculty
        fields = "__all__"


class FacultyDepartmentInfoSerializer(serializers.ModelSerializer):
    high_school_faculty = HighSchoolFacultyInfoSerializer()
    department = DepartmentSerializer()

    class Meta:
        model = FacultyDepartment
        fields = "__all__"


class DepartmentSpecializationInfoSerializer(serializers.ModelSerializer):
    faculty_department = FacultyDepartmentInfoSerializer()
    specialization = SpecializationInfoSerializer()

    class Meta:
        model = DepartmentSpecialization
        fields = "__all__"


class DepartmentSpecializationAdditionalSerializer(serializers.ModelSerializer):

    def get_name(self, instance):
        return instance.specialization.name

    def get_department(self, instance):
        return instance.faculty_department.department.name

    def get_classificator(self, instance):
        return (
            instance.specialization.classificator.name
            if instance.specialization.classificator
            else "Ýok"
        )

    def get_male_count(self, instance):
        return Student.objects.filter(
            specialization=instance,
            gender="M",
            is_expelled=False,
            is_obsolete=False,
        ).count()

    def get_female_count(self, instance):
        return Student.objects.filter(
            specialization=instance,
            gender="F",
            is_expelled=False,
            is_obsolete=False,
        ).count()

    def get_students_count(self, instance):
        return Student.objects.filter(
            specialization=instance,
            is_expelled=False,
            is_obsolete=False,
        ).count()

    name = serializers.SerializerMethodField()
    department = serializers.SerializerMethodField()
    classificator = serializers.SerializerMethodField()
    male_count = serializers.SerializerMethodField()
    female_count = serializers.SerializerMethodField()
    students_count = serializers.SerializerMethodField()

    class Meta:
        model = DepartmentSpecialization
        fields = (
            "id",
            "name",
            "department",
            "classificator",
            "male_count",
            "female_count",
            "students_count",
        )


class SpecializationAdditionalAdminSerializer(serializers.ModelSerializer):

    def get_name(self, instance):
        return instance.name

    def get_classificator(self, instance):
        return instance.classificator.name if instance.classificator else "Ýok"

    def get_male_count(self, instance):
        return Student.objects.filter(
            specialization__specialization=instance,
            gender="M",
            is_expelled=False,
            is_obsolete=False,
        ).count()

    def get_female_count(self, instance):
        return Student.objects.filter(
            specialization__specialization=instance,
            gender="F",
            is_expelled=False,
            is_obsolete=False,
        ).count()

    def get_students_count(self, instance):
        return Student.objects.filter(
            specialization__specialization=instance,
            is_expelled=False,
            is_obsolete=False,
        ).count()

    name = serializers.SerializerMethodField()
    classificator = serializers.SerializerMethodField()
    male_count = serializers.SerializerMethodField()
    female_count = serializers.SerializerMethodField()
    students_count = serializers.SerializerMethodField()

    class Meta:
        model = DepartmentSpecialization
        fields = (
            "id",
            "name",
            "classificator",
            "male_count",
            "female_count",
            "students_count",
        )


class StudentInfoSerializer(serializers.ModelSerializer):
    high_school = HighSchoolInfoSerializer()
    nationality = NationalitySerializer()
    country = CountrySerializer()
    region = RegionSerializer()
    specialization = DepartmentSpecializationInfoSerializer()

    class Meta:
        model = Student
        fields = "__all__"


class GraduateInfoSerializer(serializers.ModelSerializer):
    high_school = HighSchoolInfoSerializer()
    nationality = NationalitySerializer()
    country = CountrySerializer()
    region = RegionSerializer()
    specialization = DepartmentSpecializationInfoSerializer()

    study_period = serializers.SerializerMethodField()

    def get_study_period(self, instance):
        admission_year = instance.admission_date.year
        return f"{admission_year}-{admission_year + instance.specialization.specialization.degree.duration}"

    class Meta:
        model = Student
        fields = (
            "full_name",
            "gender",
            "family_status",
            "payment_type",
            "high_school",
            "nationality",
            "country",
            "region",
            "specialization",
            "birth_date",
            "admission_date",
            "registered_place",
            "study_year",
            "phone_number",
            "passport",
            "military_service",
            "label",
            "active",
            "study_period",
        )


class ExpelledStudentInfoSerializer(serializers.ModelSerializer):
    high_school = HighSchoolInfoSerializer()
    nationality = NationalitySerializer()
    country = CountrySerializer()
    region = RegionSerializer()
    specialization = DepartmentSpecializationInfoSerializer()
    expulsion_request = serializers.SerializerMethodField()

    def get_expulsion_request(self, instance):
        return (
            ExpulsionRequest.objects.filter(
                student=instance, verdict="C", is_obsolete=False
            )
            .last()
            .id
        )

    class Meta:
        model = Student
        fields = (
            "full_name",
            "gender",
            "family_status",
            "payment_type",
            "high_school",
            "nationality",
            "country",
            "region",
            "specialization",
            "birth_date",
            "admission_date",
            "registered_place",
            "study_year",
            "phone_number",
            "passport",
            "military_service",
            "label",
            "active",
            "is_expelled",
            "expulsion_request",
        )


class DiplomaRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiplomaRequest
        fields = "__all__"


# Teacher statement serializer


class TeacherStatementSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherStatement
        fields = "__all__"


# Custom function serializers


# Diploma serializers


def advanced_diploma_serializer(diploma_request: DiplomaRequest) -> dict:
    response = {
        "id": diploma_request.id,
        "allowed_until": diploma_request.allowed_until.astimezone(
            pytz.timezone("Asia/Ashgabat")
        ).isoformat(),
        "verdict": diploma_request.verdict,
        "verdict_date": (
            diploma_request.verdict_date.strftime("%d.%m.%Y %H:%M:%S")
            if diploma_request.verdict_date
            else None
        ),
        "request_date": diploma_request.request_date.strftime("%d.%m.%Y %H:%M:%S"),
        "original_requested_quantity": diploma_request.simple_diploma_count
        + diploma_request.honor_diploma_count,
        "honor_diplomas_quantity": diploma_request.honor_diploma_count,
        "simple_diplomas_quantity": diploma_request.simple_diploma_count,
        "total_requested_quantity": 0,
        "spare_diplomas": diploma_request.simple_diploma_count
        + diploma_request.honor_diploma_count,
        "two_year_work_off": 0,
        "died": 0,
        "went_abroad": 0,
        "other_reasons": 0,
    }
    for diploma_request_action in DiplomaRequestAction.objects.filter(
        diploma_request=diploma_request, verdict="C"
    ):
        response["spare_diplomas"] += diploma_request_action.update_simple_to
        response["spare_diplomas"] += diploma_request_action.update_honor_to
        response["simple_diplomas_quantity"] += diploma_request_action.update_simple_to
        response["honor_diplomas_quantity"] += diploma_request_action.update_honor_to
    response["total_requested_quantity"] = response["spare_diplomas"]
    for diploma_report in DiplomaReport.objects.filter(
        diploma_request=diploma_request, verdict="C"
    ):
        response["two_year_work_off"] += diploma_report.two_year_work_off
        response["died"] += diploma_report.died
        response["went_abroad"] += diploma_report.went_abroad
        response["other_reasons"] += diploma_report.other_reasons
        response["spare_diplomas"] -= (
            diploma_report.two_year_work_off
            + diploma_report.died
            + diploma_report.went_abroad
            + diploma_report.other_reasons
        )

    return response
