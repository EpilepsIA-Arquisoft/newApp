from rest_framework import serializers

from resultado.models import Resultado
from .models import Examen

class ExamenSerializer(serializers.ModelSerializer):
    # El campo 'resultado' es opcional y puede ser null
    resultado = serializers.PrimaryKeyRelatedField(queryset=Resultado.objects.all(), required=False, allow_null=True)

    class Meta:
        model = Examen
        fields = '__all__'
