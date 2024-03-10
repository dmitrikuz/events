from django.apps import apps
from django.contrib.auth import get_user_model
from django.db import models


class Organization(models.Model):
    title = models.CharField(max_length=30, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    address = models.CharField(max_length=50, verbose_name="Адресc")
    postcode = models.PositiveIntegerField(verbose_name="Почтовый индекс")


class Event(models.Model):
    title = models.CharField(max_length=30, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    organizations = models.ManyToManyField(
        to=Organization,
        related_name="events"
    )
    image = models.ImageField(verbose_name="Изображение", null=True)
    date = models.DateField(verbose_name="Дата")

    def get_participants(self):
        user_model = get_user_model()
        participants = user_model.objects.none()

        for org in self.organizations.all():
            participants = participants.union(org.users.all())
        return participants
