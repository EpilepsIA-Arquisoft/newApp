from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from .models import Examen
from .serializers import ExamenSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from resultado.serializers import ResultadoSerializer

class ExamenListCreateView(generics.ListCreateAPIView):
    queryset = Examen.objects.all()
    serializer_class = ExamenSerializer

class CrearResultadoExamenView(APIView):
    def post(self, request, examen_id, *args, **kwargs):
        get_object_or_404(Examen, id=examen_id)
        serializer = ResultadoSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
