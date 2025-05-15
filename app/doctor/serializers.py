from rest_framework import serializers
from .models import Doctor
from django.contrib.auth import authenticate


class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = '__all__'

