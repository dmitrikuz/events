from django.contrib import admin
from django.utils.html import mark_safe

from .models import Event, Organization


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_filter = ["title", "date", "organizations"]
    list_display = ["title", "date", "image_preview"]

    @admin.display(description="Превью")
    def image_preview(self, obj):
        return mark_safe('<img src="{url}" width="{width}" height={height} />'.format(
            url=obj.image.url,
            width=50,
            height=50
        )
        )


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    ...
