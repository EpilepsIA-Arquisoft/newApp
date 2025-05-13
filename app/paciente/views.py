from rest_framework import generics

from doctor.serializers import DoctorSerializer
from .models import Paciente
from .serializers import PacienteSerializer
from rest_framework.permissions import IsAuthenticated
from user.permissions import RolePermissionFactory
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import Paciente
from rest_framework_simplejwt.authentication import JWTAuthentication

class PacienteListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, RolePermissionFactory(['admin'])]
    queryset = Paciente.objects.all()
    serializer_class = PacienteSerializer

class PacientesPorDoctorView(APIView):
    permission_classes = [IsAuthenticated, RolePermissionFactory(['doctor'])]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        try:
            # Obtener el doctor logueado
            user = request.user
            #doctorS = DoctorSerializer(doctor)

            # Verificar si el doctor tiene el rol de "doctor"
            if user.rol != 'doctor':
                return Response({"detail": "No tiene permiso para ver pacientes."}, status=status.HTTP_403_FORBIDDEN)

            # Obtener todos los pacientes del doctor logueado
            pacientes = Paciente.objects.filter(doctor=user)

            # Serializar los pacientes
            serializer = PacienteSerializer(pacientes, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({"detail": f"Error al obtener los pacientes: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)