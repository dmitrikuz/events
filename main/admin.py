from django.contrib import admin

from .models import Event, Organization


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    ...


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    ...
