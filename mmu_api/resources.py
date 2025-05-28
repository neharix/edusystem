from import_export import resources

from .models import EducationCenter, File, Specialization, Staff


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
