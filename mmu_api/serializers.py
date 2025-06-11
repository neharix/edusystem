from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer, SerializerMethodField

from .models import (
    Achievement,
    Certificate,
    Country,
    Course,
    Direction,
    EducationCenter,
    File,
    Nationality,
    Profile,
    Region,
    Specialization,
    Staff,
    Student,
)


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username")


class ProfileSerializer(ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Profile
        fields = ("id", "user")


class FileSerializer(ModelSerializer):
    uploader = ProfileSerializer()
    to = ProfileSerializer()

    class Meta:
        fields = "__all__"
        model = File


class SpecializationSerializer(ModelSerializer):
    class Meta:
        model = Specialization
        fields = "__all__"


class SpecializationAdditionalSerializer(ModelSerializer):

    class Meta:
        fields = ["id", "name"]
        model = Specialization


class CountrySerializer(ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Country


class RegionSerializer(ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Region


class NationalitySerializer(ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Nationality


class StaffSerializer(ModelSerializer):
    specializations = SpecializationSerializer(many=True)
    country = CountrySerializer()
    region = RegionSerializer()

    class Meta:
        fields = "__all__"
        model = Staff


class ProfileAdditionalSerializer(ModelSerializer):

    def get_user_id(self, instance: Profile):
        return instance.user.id

    def get_username(self, instance: Profile):
        return instance.user.username

    def get_email(self, instance: Profile):
        return instance.user.email

    user_id = SerializerMethodField()
    username = SerializerMethodField()
    email = SerializerMethodField()

    class Meta:
        model = Profile
        fields = ("id", "user_id", "username", "email", "role")


class EducationCenterSerializer(ModelSerializer):
    class Meta:
        model = EducationCenter
        fields = "__all__"


class EducationCenterAdditionalSerializer(ModelSerializer):
    def get_students_count(self, instance: EducationCenter):
        return 10

    students_count = SerializerMethodField()

    class Meta:
        model = EducationCenter
        fields = ("id", "name", "students_count")


class AboutEducationCenterSerializer(ModelSerializer):
    def get_country(self, instance: EducationCenter):
        return instance.country.name

    def get_region(self, instance: EducationCenter):
        return instance.region.name

    country = SerializerMethodField()
    region = SerializerMethodField()

    class Meta:
        model = EducationCenter
        fields = (
            "id",
            "name",
            "phone_number",
            "lat",
            "lng",
            "country",
            "region",
            "address",
            "is_active",
            "buildings_count",
            "rooms_count",
            "capacity",
            "books_count",
        )


class AchievementSerializer(ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Achievement


class AchievementAdditionalSerializer(ModelSerializer):
    def get_students_count(self, instance: Achievement):
        return 10

    def get_female_count(self, instance: Achievement):
        return 10

    def get_male_count(self, instance: Achievement):
        return 10

    students_count = SerializerMethodField()
    female_count = SerializerMethodField()
    male_count = SerializerMethodField()

    class Meta:
        fields = ["id", "name", "students_count", "male_count", "female_count"]
        model = Achievement


class StudentAdditionalSerializer(ModelSerializer):

    class Meta:
        model = Student
        fields = ("id", "full_name")


class StudentSerializer(ModelSerializer):
    class Meta:
        model = Student
        fields = "__all__"


class DirectionSerializer(ModelSerializer):
    class Meta:
        model = Direction
        fields = "__all__"


class CourseSerializer(ModelSerializer):
    education_center = EducationCenterSerializer()
    direction = DirectionSerializer()

    class Meta:
        model = Course
        fields = "__all__"


class CertificateSerializer(ModelSerializer):
    education_center = EducationCenterSerializer()
    student = StudentSerializer()
    course = CourseSerializer()

    class Meta:
        model = Certificate
        fields = "__all__"
