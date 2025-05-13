from rest_framework import generics
from .models import Resultado
from .serializers import ResultadoSerializer
from rest_framework.permissions import IsAuthenticated
from user.permissions import RolePermissionFactory

class ResultadoListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated, RolePermissionFactory(['admin'])]
    queryset = Resultado.objects.all()
    serializer_class = ResultadoSerializer
    
class ResultadoCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated, RolePermissionFactory(['admin','reducer'])]
    queryset = Resultado.objects.all()
    serializer_class = ResultadoSerializer