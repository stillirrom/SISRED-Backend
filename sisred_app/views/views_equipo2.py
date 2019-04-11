from django.core.serializers import serialize
from rest_framework import serializers
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from sisred_app.models import ProyectoRED, Recurso, RED, RolAsignado, Perfil, Rol, Version
from django.contrib.auth.models import User

@csrf_exempt
def getProyectosRED(request):
    vLstObjects = list(ProyectoRED.objects.all())
    return HttpResponse(serialize('json', vLstObjects), content_type="application/json")

@csrf_exempt
def getRecurso(request):
    vLstObjects = list(Recurso.objects.all())
    return HttpResponse(serialize('json', vLstObjects), content_type="application/json")

@csrf_exempt
def getRED(request):
    vLstObjects = list(RED.objects.all())
    return HttpResponse(serialize('json', vLstObjects), content_type="application/json")


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')


class PerfilSerializer(serializers.ModelSerializer):
    usuario = UserSerializer()
    class Meta:
        model = Perfil
        fields = '__all__'


class RedSerializer(serializers.ModelSerializer):
    class Meta:
        model = RED
        fields = '__all__'


class RolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rol
        fields = '__all__'


class RolAsignadoSerializer(serializers.ModelSerializer):
    red = RedSerializer()
    usuario = PerfilSerializer()
    rol = RolSerializer()
    class Meta:
        model = RolAsignado
        fields = ('red', 'rol', 'usuario')


class VersionSerializer(serializers.ModelSerializer):
    creado_por = PerfilSerializer()
    class Meta:
        model = Version
        fields= '__all__'


@csrf_exempt
def getAsignaciones(request):
    data = list(RolAsignado.objects.all())
    serializer = RolAsignadoSerializer(data, many=True)
    return JsonResponse({'context': serializer.data}, safe=True)


@csrf_exempt
def getVersionesRED(request, id):
    data = Version.objects.filter(red_id=id).order_by('numero')
    serializer = VersionSerializer(data, many=True)
    return JsonResponse({'context': serializer.data}, safe=True)
