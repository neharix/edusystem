from django.contrib.auth.models import User
from rest_framework import serializers

from .models import (
    Classificator,
    Degree,
    Department,
    Faculty,
    HighSchool,
    Nationality,
    Profile,
    Specialization,
    Student,
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


class NationalitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Nationality
        fields = "__all__"
