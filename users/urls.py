from django.contrib.auth.views import LoginView, LogoutView
from django.urls import include, path

from .api.views import TokenObtainPairView, TokenRefreshView, UserCreateView
from .views import SignupView

api_patterns = [
    path("", UserCreateView.as_view()),
    path("jwt/obtain", TokenObtainPairView.as_view()),
    path("jwt/refresh", TokenRefreshView.as_view())
]
urlpatterns = [
    path("api/", include(api_patterns)),
    path("signup/", SignupView.as_view(), name="signup"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout")
]
