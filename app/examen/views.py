from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from .models import Examen
from .serializers import ExamenSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from resultado.serializers import ResultadoSerializer
from rest_framework.permissions import IsAuthenticated
from user.permissions import RolePermissionFactory

class ExamenListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated, RolePermissionFactory(['admin'])]
    queryset = Examen.objects.all()
    serializer_class = ExamenSerializer

class ExamenCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated, RolePermissionFactory(['admin','uploader'])]
    queryset = Examen.objects.all
    serializer_class = ExamenSerializer
class ResultadoExamenCreateView(APIView):
    permission_classes = [IsAuthenticated, RolePermissionFactory(['admin', 'reducer'])]
    def post(self, request, examen_id, *args, **kwargs):
        examen = get_object_or_404(Examen, id=examen_id)
        serializer = ResultadoSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            examen.resultado = serializer.instance
            examen.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ResultadoExamenDetailView(APIView):
    permission_classes = [IsAuthenticated, RolePermissionFactory(['admin',"doctor"])]
    def get(self, request, examen_id, *args, **kwargs):
        user= request.user
        examen = get_object_or_404(Examen, id=examen_id)
        if user!=examen.paciente.doctor:
            return Response({"detail": "No tienes permiso para ver este examen."}, status=status.HTTP_403_FORBIDDEN)
        resultado = examen.resultado
        
        if resultado:
            serializer = ResultadoSerializer(resultado)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "No se encontró el resultado para este examen."}, status=status.HTTP_404_NOT_FOUND)
