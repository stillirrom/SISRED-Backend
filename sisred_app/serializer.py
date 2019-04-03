from .models import Recurso, RED
from rest_framework import  serializers

class RecursoSerializer(serializers.ModelSerializer):
    class Meta:
        model=Recurso
        fields=('nombre','archivo','thumbnail','fecha_creacion','fecha_ultima_modificacion','tipo','descripcion','metadata','autor','usuario_ultima_modificacion','getAutor','getResponsableModificacion')


class HistorialFaseSerilaizer(serializers.ModelSerializer):
    class Meta:
        model = RED
        fileds = '__all__'


class REDSerializer(serializers.ModelSerializer):
    class Meta:
        model = RED
        fields = ('id_conectate', 'nombre', 'nombre_corto', 'descripcion', 'fecha_inicio',
                  'fecha_cierre', 'fecha_creacion', 'porcentaje_avance', 'tipo', 'solicitante', 'proyecto_conectate', 'horas_estimadas',
                  'horas_trabajadas')