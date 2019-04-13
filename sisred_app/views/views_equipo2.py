from django.shortcuts import get_object_or_404,get_list_or_404
from django.core import serializers
from django.core.serializers import serialize
from rest_framework import serializers
from django.http import HttpResponse, JsonResponse, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
from sisred_app.models import ProyectoRED, Recurso, RED, RolAsignado, Perfil, Rol, Version
from django.db.models import Q
from django.contrib.auth.models import User
from datetime import datetime
import json

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
    
def buscarRed(request):
    if request.method == 'GET':
        fstart = request.GET.get("fstart")
        fend = request.GET.get("fend")
        text = request.GET.get("text")
        
        q = RED.objects.filter() 

        if text:
            q = q.filter(Q(nombre__contains=text) | Q(nombre_corto__contains=text)  | Q(descripcion__contains=text) | Q(metadata__tag=text))
        
        if fend:
            q = q.filter(fecha_cierre__lte = fend)
        
        if fstart:
            q = q.filter(fecha_inicio__gte = fstart)

        return JsonResponse(list(q.values()),safe=False)
    return HttpResponseNotFound()     

def versiones(request):
    if request.method == 'POST':
        data = jsonUser = json.loads(request.body)
        es_final = False
        
        imagen = data['imagen']
        archivos = data['archivos']
        redId = data['redId']
        fecha_creacion = datetime.now()

        idRecursos = data['recursos']

        red = get_object_or_404(RED, id = redId)
        
        oldVersions = Version.objects.filter(red__id = redId).values()
        
        numero = 1
        print("old: " + str(len(oldVersions)))
        if len(oldVersions) > 0:
            numero = max((v.numero for v in oldVersions)) + 1 
        
        print("nuuuuumero:" + str(numero))
        recursos =  Recurso.objects.filter(id__in = idRecursos)
        
        #creadoPor = traer el objeto del request

        version = Version.objects.create(
            es_final = es_final,
            imagen = imagen,
            archivos=archivos,
            red=red,
            numero=numero,
            #creadoPor=creadoPor,
            fecha_creacion=fecha_creacion
        )
        #falta agregar los recursos a la version
        version.recursos.set(recursos)
        #
        version.save()   
        #falta retornar con el serilizer
        #y quitar que sea un vector para que solo retorne el objero

        return HttpResponse(serialize('json',[version]))
    return HttpResponseNotFound()   


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name')


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


@csrf_exempt
def getAsignaciones(request):
    data = list(RolAsignado.objects.all())
    serializer = RolAsignadoSerializer(data, many=True)
    return JsonResponse({'context': serializer.data}, safe=True)
