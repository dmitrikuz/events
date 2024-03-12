from django.contrib import admin

from .models import Event, Organization


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_filter = ["title", "date", "organizations__title"]


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    ...
