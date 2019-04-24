from django.shortcuts import get_object_or_404,get_list_or_404
from django.core import serializers
from django.core.serializers import serialize
from rest_framework import serializers
from django.http import HttpResponse, JsonResponse, HttpResponseNotFound, Http404
from sisred_app.models import ProyectoRED, Recurso, RED, RolAsignado, Perfil, Rol, Version
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from sisred_app.models import ProyectoRED, Recurso, RED, RolAsignado, Perfil, Rol, ProyectoConectate, Version
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from sisred_app.serializer import RecursoSerializer
from datetime import datetime

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

@csrf_exempt
def marcarVersion(request,id):
    if request.method == 'POST':
        version = get_object_or_404(Version, id=id)

        otherVersions = get_list_or_404(Version, red_id = version.red_id)
        for v in otherVersions:
            v.es_final=False
            v.save()

        version.es_final = True
        version.save()
        return JsonResponse(str(id), safe=False)    
    return HttpResponseNotFound()     
    
def buscarRed(request, idUsuario):
    if request.method == 'GET':
        fstart = request.GET.get("fstart")
        fend = request.GET.get("fend")
        text = request.GET.get("text")
        
        usuario = User.objects.get(pk=idUsuario);
        perfil = Perfil.objects.get(usuario=usuario);
        roles_asignado = RolAsignado.objects.filter(usuario=perfil)

        q = RED.objects.filter(rolasignado__in=roles_asignado) 

        if text:
            q = q.filter(Q(nombre__contains=text) | Q(nombre_corto__contains=text)  | Q(descripcion__contains=text) | Q(metadata__tag=text))
        
        if fend:
            q = q.filter(fecha_cierre__lte = fend)
        
        if fstart:
            q = q.filter(fecha_inicio__gte = fstart)

        return JsonResponse(list(q.values()),safe=False)
    return HttpResponseNotFound()     


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


class ProyectoSerializer_v(serializers.ModelSerializer):
    class Meta:
        model = ProyectoConectate
        fields = ('nombre',)

class RedSerializer_v(serializers.ModelSerializer):
    proyecto_conectate = ProyectoSerializer_v()
    class Meta:
        model = RED
        fields = ('nombre', 'proyecto_conectate')

class VersionSerializer_v(serializers.ModelSerializer):
    red = RedSerializer_v()
    creado_por = PerfilSerializer()
    class Meta:
        model = Version
        fields = ('numero', 'imagen', 'creado_por', 'fecha_creacion', 'red')


@csrf_exempt
def getVerVersion(request, id):
    version = get_object_or_404(Version, id=id)

    serializer = VersionSerializer_v(version, many=False)
    return JsonResponse(serializer.data, safe=True)


@csrf_exempt
def getVerVersionR(request, id):
    version = get_object_or_404(Version, id=id)

    serializer = RecursoSerializer(version.recursos, many=True)
    return JsonResponse({'context':serializer.data}, safe=True)


@csrf_exempt
def getVersionesRED(request, id):
    try:
        red = RED.objects.get(pk=id)
    except:
        raise Http404('No existe un RED con id '+str(id))
    data = Version.objects.filter(red=red).order_by('numero')
    serializer = VersionSerializer(data, many=True)
    return JsonResponse({'context': serializer.data}, safe=True)
