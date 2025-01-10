from rest_framework import serializers

from .models import (
    Classificator,
    Degree,
    Department,
    HighSchool,
    Specialization,
    Student,
)


class HighSchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = HighSchool
        fields = "__all__"


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = "__all__"


class DegreeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Degree
        fields = "__all__"


class ClassificatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classificator
        fields = "__all__"


class SpecializationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialization
        fields = "__all__"


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = "__all__"
