from rest_framework import serializers
from .models import Solicitud

class SolicitudSerializer(serializers.ModelSerializer):
    class Meta:
        model = Solicitud
        fields = '__all__'
        read_only_fields = ['doctor']

    def validate(self, data):
        # El doctor será asignado en perform_create, pero validamos aquí por seguridad
        request = self.context['request']
        examen = data.get('examen')
        if examen.paciente.doctor != request.user:
            raise serializers.ValidationError("No tienes permiso para ver este examen.")
        return data

    def create(self, validated_data):
        examen = validated_data['examen']
        msj = {
            "id_paciente": examen.paciente.id,
            "id_examen": examen.id,
            "ubicacion_examen": examen.url,
        }
        from rabbit_writer.writer import publish_message
        publish_message('map_requests', msj)
        return super().create(validated_data)
