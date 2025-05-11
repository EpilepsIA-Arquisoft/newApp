from rest_framework import generics
from .models import Solicitud
from .serializers import SolicitudSerializer

class SolicitudListCreateView(generics.ListCreateAPIView):
    queryset = Solicitud.objects.all()
    serializer_class = SolicitudSerializer
