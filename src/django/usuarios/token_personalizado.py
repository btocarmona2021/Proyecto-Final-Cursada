# usuarios/token_personalizado.py
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Agregar claims custom al token JWT (payload interno)
        token["username"] = user.username
        token["email"] = user.email

        return token

    def validate(self, attrs):
        data = super().validate(attrs)

        # Agregar datos extra a la RESPUESTA del endpoint (no al token)
        data["user_id"] = self.user.id
        data["username"] = self.user.username
        data["email"] = self.user.email

        # Agregar grupo si existe
        if self.user.is_staff:
            data["grupo"] = "administradores"
        else:
            first_group = self.user.groups.first()
            data["grupo"] = first_group.name if first_group else None
        return data


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    throttle_scope = "login"


class LogoutView(APIView):
    """Invalida el refresh token al cerrar sesion."""

    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh = request.data.get("refresh")
        if refresh:
            token = RefreshToken(refresh)
            token.blacklist()
        return Response(status=status.HTTP_204_NO_CONTENT)
