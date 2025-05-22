from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken

from django.contrib.auth import get_user_model
from .models import BlacklistedToken

from .permissions import IsDoctor, IsBotReduce, IsBotExamenUploader, IsAdmin

User = get_user_model()

# Serializador personalizado para incluir más datos del usuario en el token
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data.update({
            'user_id': self.user.username,
            'nombre': self.user.nombre,
            'rol': self.user.rol,
        })
        return data

# Vista para obtener el token JWT
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        try:
            # Verificar el header de autorización
            auth_header = request.headers.get("Authorization")
            if not auth_header or not auth_header.startswith("Bearer "):
                return Response(
                    {"detail": "Token de acceso no proporcionado o formato inválido"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Extraer el access token
            access_token = auth_header.split(" ")[1]
            
            # Verificar el refresh token en el body
            refresh_token = request.data.get("refresh")
            if not refresh_token:
                return Response(
                    {"detail": "Refresh token no proporcionado"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            try:
                # Intentar invalidar el refresh token
                token = RefreshToken(refresh_token)
                token.blacklist()
            except TokenError:
                return Response(
                    {"detail": "Refresh token inválido o expirado"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Verificar si el access token ya está en la blacklist
            if BlacklistedToken.objects.filter(token=access_token).exists():
                return Response(
                    {"detail": "Token de acceso ya ha sido invalidado"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Agregar el access token a la blacklist
            BlacklistedToken.objects.create(token=access_token)

            # Crear la respuesta
            response = Response(
                {"detail": "Logout exitoso"},
                status=status.HTTP_205_RESET_CONTENT
            )

            # Limpiar las cookies si existen
            response.delete_cookie('access_token')
            response.delete_cookie('refresh_token')

            return response

        except Exception as e:
            return Response(
                {
                    "detail": "Error durante el proceso de logout",
                    "error": str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

# Vista para obtener los datos del usuario autenticado
class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        print(">>> DEBUG: Usuario autenticado:", request.user)
        return Response({
            'id': request.user.id,
            'nombre': request.user.nombre,
            'rol': request.user.rol,
        })

# Vista protegida para rol doctor
class DoctorDashboardView(APIView):
    permission_classes = [IsAuthenticated, IsDoctor]

    def get(self, request):
        return Response({"mensaje": "Bienvenido doctor"})

# Vista protegida para rol bot_reducer
class BotReducerTaskView(APIView):
    permission_classes = [IsAuthenticated, IsBotReduce]

    def get(self, request):
        return Response({"mensaje": "Tareas del bot reducer"})

# Vista protegida para rol bot_examen_uploader
class BotExamenUploaderTaskView(APIView):
    permission_classes = [IsAuthenticated, IsBotExamenUploader]

    def get(self, request):
        return Response({"mensaje": "Tareas del bot examen uploader"})

# Vista protegida para rol admin
class AdminPanelView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request):
        return Response({"mensaje": "Panel de administración"})

class AdminListUsersView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request):
        try:
            # Obtener todos los usuarios
            users = User.objects.all()
            user_data = [{
                "id": user.id,
                "nombre": user.nombre,
                "rol": user.rol,
            } for user in users]

            return Response({"usuarios": user_data}, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({"detail": f"Error al obtener los usuarios: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)