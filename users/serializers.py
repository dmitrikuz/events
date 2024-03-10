from rest_framework.serializers import ModelSerializer

from .models import CustomUser


class SignupSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ("email", "password")


class ReadSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ("email", "organization", "phone_number")


# TODO Refactor As CreateView
