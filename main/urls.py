from django.urls import path

from .views import (EventsByParticipantsListView, EventsCreateView,
                    FilteredEventsListView, OrganizationListView)

urlpatterns = [

    path("organizations", OrganizationListView.as_view()),
    path("events", EventsCreateView.as_view()),
    path("events/participants", EventsByParticipantsListView.as_view()),
    path("events/filtered", FilteredEventsListView.as_view()),
]
