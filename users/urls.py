from django.urls import path

from .views import TokenObtainPairView, TokenRefreshView, UserViewSet

urlpatterns = [
    path("", UserViewSet.as_view({"post": "create"})),

    path("jwt/obtain", TokenObtainPairView.as_view()),
    path("jwt/refresh", TokenRefreshView.as_view())
]
