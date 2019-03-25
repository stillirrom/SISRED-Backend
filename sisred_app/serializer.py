from .models import  Recurso
from rest_framework import  serializers

class RecursoSerializer(serializers.ModelSerializer):
    class Meta:
        model=Recurso
        field=('nombre','archivo','thumbnail','fecha_creacion','fecha_ultima_modificacion','tipo','descripcion','autor','usuario_ultima_modificacion')

