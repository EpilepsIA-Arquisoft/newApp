from rest_framework import generics
from .models import Doctor
from .serializers import DoctorSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAuthenticated
from user.permissions import RolePermissionFactory

class DoctorCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated, RolePermissionFactory(['admin'])]
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer

class DoctorListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated, RolePermissionFactory(['admin'])]
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer