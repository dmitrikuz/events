from django.urls import path

from . import views

urlpatterns = [

    path("organizations", views.OrganizationCreateView.as_view()),
    path("events", views.EventsCreateView.as_view()),
    path("events/<int:pk>/participants",
         views.EventParticipantsDetailView.as_view()),
    path("events/filtered", views.FilteredEventsListView.as_view()),
]
