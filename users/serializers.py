from rest_framework.serializers import ModelSerializer

from .models import CustomUser


class SignupSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ("email", "password")

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user


class ReadSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ("email", "organization", "phone_number")
