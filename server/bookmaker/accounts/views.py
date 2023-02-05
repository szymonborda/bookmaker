from rest_framework import views, permissions, status, generics
from rest_framework.response import Response
from bookmaker.accounts.serializers import AccountSerializer, LoginSerializer
from django.contrib.auth import login, logout


class ProfileView(generics.RetrieveAPIView):
    serializer_class = AccountSerializer

    def get_object(self):
        return self.request.user


class LoginView(views.APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = LoginSerializer(
            data=self.request.data,
            context={"request": self.request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        login(request, user)
        return Response(None, status=status.HTTP_202_ACCEPTED)


class LogoutView(views.APIView):
    def post(self, request, format=None):
        logout(request)
        return Response(None, status=status.HTTP_202_ACCEPTED)
