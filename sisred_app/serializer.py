from .models import  Recurso
from rest_framework import  serializers

class RecursoSerializer(serializers.ModelSerializer):
    class Meta:
        model=Recurso
        fields=('nombre','archivo','thumbnail','fecha_creacion','fecha_ultima_modificacion','tipo','descripcion','metadata','autor','usuario_ultima_modificacion')

