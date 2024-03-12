from django.urls import path

from .views import TokenObtainPairView, TokenRefreshView, UserCreateView

urlpatterns = [
    path("", UserCreateView.as_view()),
    path("jwt/obtain", TokenObtainPairView.as_view()),
    path("jwt/refresh", TokenRefreshView.as_view())
]
