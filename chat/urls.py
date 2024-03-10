from django.urls import include, path

from . import views

urlpatterns = [
    path("", views.index),
    path("<str:room_name>/", views.room)
]
