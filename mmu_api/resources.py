from import_export import resources

from .models import (
    Achievement,
    Certificate,
    Course,
    Direction,
    EducationCenter,
    File,
    Specialization,
    Staff,
    Student,
)


class EducationCenterResource(resources.ModelResource):
    class Meta:
        model = EducationCenter


class FileResource(resources.ModelResource):
    class Meta:
        model = File


class StaffResource(resources.ModelResource):
    class Meta:
        model = Staff


class SpecializationResource(resources.ModelResource):
    class Meta:
        model = Specialization


class AchievementResource(resources.ModelResource):
    class Meta:
        model = Achievement


class DirectionResource(resources.ModelResource):
    class Meta:
        model = Direction


class CourseResource(resources.ModelResource):
    class Meta:
        model = Course


class CertificateResource(resources.ModelResource):
    class Meta:
        model = Certificate


class StudentResource(resources.ModelResource):
    class Meta:
        model = Student
