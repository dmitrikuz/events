from rest_framework.generics import CreateAPIView
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from users.models import CustomUser

from .serializers import SignupSerializer


class UserCreateView(CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = SignupSerializer
