from celery import shared_task

from .models import Event


@shared_task
def create_event(event_data):
    organizations_pks = event_data.pop("organizations")
    obj = Event.objects.create(**event_data)
    obj.organizations.set(organizations_pks)
    return obj.pk
