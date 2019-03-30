from .models import Recurso, HistorialFase, RED
from rest_framework import  serializers

class RecursoSerializer(serializers.ModelSerializer):
    class Meta:
        model=Recurso
        fields=('nombre','archivo','thumbnail','fecha_creacion','fecha_ultima_modificacion','tipo','descripcion','metadata','autor','usuario_ultima_modificacion','getAutor','getResponsableModificacion')


class HistorialFaseSerilaizer(serializers.ModelSerializer):
    class Meta:
        model = RED
        fileds = '__all__'


class FaseSerializer(serializers.ModelSerializer):
    red = HistorialFaseSerilaizer(many=True)
    class Meta:
        model=HistorialFase
        fields='__all__'