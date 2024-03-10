from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from .models import CustomUser
from .serializers import ReadSerializer, SignupSerializer


class UserViewSet(ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = ReadSerializer

    def get_serializer_class(self):
        if self.action == "create":
            return SignupSerializer

        return super().get_serializer_class()
