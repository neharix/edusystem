from django.contrib.auth.models import User
from parler_rest.serializers import TranslatableModelSerializer, TranslatedFieldsField
from rest_framework.serializers import ModelSerializer, SerializerMethodField

from main.models import Country, Profile, Region

from .models import EducationCenter, File, Specialization, Staff


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


class SpecializationSerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=Specialization)

    class Meta:
        model = Specialization
        fields = ["id", "translations"]


class CountrySerializer(ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Country


class RegionSerializer(ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Region


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
