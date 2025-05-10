from rest_framework.serializers import ModelSerializer, SerializerMethodField

from api.models import Profile


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
