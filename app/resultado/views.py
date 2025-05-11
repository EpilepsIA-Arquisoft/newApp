from rest_framework import generics
from .models import Resultado
from .serializers import ResultadoSerializer

class ResultadoListCreateView(generics.ListCreateAPIView):
    queryset = Resultado.objects.all()
    serializer_class = ResultadoSerializer
