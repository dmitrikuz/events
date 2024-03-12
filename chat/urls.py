from django.urls import include, path

from . import views

urlpatterns = [
    path("", views.UserChatsView.as_view(), name="chats"),
    path("<int:pk>/", views.ChatSocketView.as_view(), name="chat")
]
