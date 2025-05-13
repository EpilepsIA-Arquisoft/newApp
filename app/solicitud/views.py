from rest_framework import generics
from .models import Solicitud
from .serializers import SolicitudSerializer
from rest_framework.permissions import IsAuthenticated
from user.permissions import RolePermissionFactory
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Solicitud
from .serializers import SolicitudSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
class SolicitudListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated, RolePermissionFactory(['admin'])]
    queryset = Solicitud.objects.all()
    serializer_class = SolicitudSerializer
    
class SolicitudCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated, RolePermissionFactory(['admin'])]
    queryset = Solicitud.objects.all()
    serializer_class = SolicitudSerializer

class SolicitudesPorDoctorView(APIView):
    permission_classes = [IsAuthenticated, RolePermissionFactory(['doctor'])]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        try:
            # Obtener el doctor logueado
            user = request.user

            # Obtener todas las solicitudes del doctor logueado
            solicitudes = Solicitud.objects.filter(doctor=user)

            # Serializar las solicitudes
            serializer = SolicitudSerializer(solicitudes, many=True)

            return Response({"solicitudes": serializer.data}, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({"detail": f"Error al obtener las solicitudes: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)