from django.core import serializers
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from sisred_app.models import ProyectoRED, Recurso, RED, ProyectoConectate, RolAsignado, Rol, Perfil, Estado, Fase



def getProyectosRED(request):
    vLstObjects = list(ProyectoRED.objects.all())
    return HttpResponse(serializers.serialize('json', vLstObjects), content_type="application/json")

def getRecurso(request):
    vLstObjects = list(Recurso.objects.all())
    return HttpResponse(serializers.serialize('json', vLstObjects), content_type="application/json")

def getRED(request):
    vLstObjects = list(RED.objects.all())
    return HttpResponse(serializers.serialize('json', vLstObjects), content_type="application/json")

def getRoles(request):
    vLstObjects = list(Rol.objects.all())
    return HttpResponse(serializers.serialize('json', vLstObjects), content_type="application/json")

def getEstados(request):
    vLstObjects = list(Estado.objects.all())
    return HttpResponse(serializers.serialize('json', vLstObjects), content_type="application/json")

def getFases(request):
    vLstObjects = list(Fase.objects.all())
    return HttpResponse(serializers.serialize('json', vLstObjects), content_type="application/json")
