from django.contrib.auth import get_user_model
from django.core.files import File
from django.core.files.storage import FileSystemStorage
from rest_framework import serializers
from rest_framework.serializers import (ModelSerializer,
                                        PrimaryKeyRelatedField,
                                        SerializerMethodField)

from .models import Event, Organization

UserModel = get_user_model()


class OrganizationCreateSerializer(ModelSerializer):
    class Meta:
        model = Organization
        fields = (
            "title",
            "description",
            "address",
            "postcode"
        )


class OrganizationReadSerializer(ModelSerializer):
    combined_address_postcode = SerializerMethodField()

    class Meta:
        model = Organization
        fields = ("id", "title", "combined_address_postcode")

    def get_combined_address_postcode(self, obj):
        return "{}, {}".format(obj.address, str(obj.postcode))


class UserFromOrganizationSerializer(ModelSerializer):
    organization = OrganizationReadSerializer()

    class Meta:
        model = UserModel
        fields = ("email", "organization")


class EventWithParticipantsReadSerializer(ModelSerializer):

    participants = UserFromOrganizationSerializer(
        source="get_participants", many=True)

    class Meta:
        model = Organization
        fields = ("id", "title", "participants")


class EventReadSerializer(ModelSerializer):
    organizations = PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Event
        fields = (
            "title",
            "description",
            "image",
            "organizations",
            "date"
        )


class PrimaryKeyCreateField(serializers.PrimaryKeyRelatedField):

    """
        Используется pk вместо объектов модели
    """

    def to_internal_value(self, data):
        return super().to_internal_value(data).pk


class EventCreateSerializer(EventReadSerializer):
    organizations = PrimaryKeyCreateField(
        queryset=Organization.objects.all(),
        many=True,
        write_only=True
    )

    # Необходимо загрузить файл, а потом передать его url в задачу Celery
    def validate_image(self, value: File):
        storage = FileSystemStorage()
        storage.save(value.name, File(value))
        return value.name
