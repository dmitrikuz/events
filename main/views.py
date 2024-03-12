from django.conf import settings
from rest_framework import pagination, status
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .filters import EventsFilterBackend
from .models import Event, Organization
from .serializers import (EventCreateSerializer, EventReadSerializer,
                          EventWithParticipantsReadSerializer,
                          OrganizationCreateSerializer)
from .tasks import create_event


class EventsPagination(pagination.LimitOffsetPagination):
    default_limit = 5


class FilteredEventsListView(ListAPIView):
    queryset = Event.objects.all()
    serializer_class = EventReadSerializer
    filter_backends = (EventsFilterBackend, )
    permission_classes = [IsAuthenticated]
    pagination_class = EventsPagination


class EventsByParticipantsListView(ListAPIView):
    queryset = Event.objects.all()
    serializer_class = EventWithParticipantsReadSerializer
    permission_classes = [IsAuthenticated]


class EventsCreateView(GenericAPIView):
    serializer_class = EventCreateSerializer
    permission_classes = [IsAuthenticated]

    def __init__(self, *args, **kwargs):
        self.delay = settings.EVENT_CREATION_TIME
        super().__init__(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        create_event.apply_async(
            args=(serializer.validated_data, ),
            countdown=self.delay
        )

        response_data = {
            "success": True,
            "message": "Creation of event {}, {} is scheduled in {} seconds".format(
                serializer.data["title"],
                serializer.data["date"],
                self.delay
            )
        }
        return Response(
            data=response_data,
            status=status.HTTP_200_OK,
        )


class OrganizationListView(ListAPIView):
    queryset = Organization.objects.all()
    serializer_class = OrganizationCreateSerializer
