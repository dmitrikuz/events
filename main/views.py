from django.conf import settings
from rest_framework import pagination, status
from rest_framework.generics import (CreateAPIView, GenericAPIView,
                                     ListAPIView, RetrieveAPIView)
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


class EventParticipantsDetailView(RetrieveAPIView):
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
            "message": "Создание мероприятия {}, {} запланировано через {} секунд".format(
                serializer.data["title"],
                serializer.data["date"],
                self.delay
            )
        }
        return Response(
            data=response_data,
            status=status.HTTP_200_OK,
        )


class OrganizationCreateView(CreateAPIView):
    queryset = Organization.objects.all()
    serializer_class = OrganizationCreateSerializer
