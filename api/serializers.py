from django.contrib.auth.models import User
from rest_framework import serializers

from .models import (
    Classificator,
    Country,
    Degree,
    Department,
    DepartmentSpecialization,
    Faculty,
    FacultyDepartment,
    HighSchool,
    HighSchoolFaculty,
    Nationality,
    Profile,
    Region,
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


class StudentAdditionalSerializer(serializers.ModelSerializer):
    high_school = HighSchoolSerializer()

    class Meta:
        model = Student
        fields = ["id", "full_name", "high_school", "study_year"]


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


class StudentInfoSerializer(serializers.ModelSerializer):
    high_school = HighSchoolInfoSerializer()
    nationality = NationalitySerializer()
    country = CountrySerializer()
    region = RegionSerializer()
    specialization = DepartmentSpecializationInfoSerializer()

    class Meta:
        model = Student
        fields = "__all__"
