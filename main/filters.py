from django_filters import rest_framework as filters

from .models import Event


class EventsFilterSet(filters.FilterSet):
    ordering = filters.OrderingFilter(fields=("date", ))
    date = filters.DateFromToRangeFilter()
    title = filters.CharFilter()

    class Meta:
        model = Event
        fields = ("ordering", "date")


class EventsFilterBackend(filters.DjangoFilterBackend):
    def get_filterset_class(self, view, queryset=None):
        return EventsFilterSet
