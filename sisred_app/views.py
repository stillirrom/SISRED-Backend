from django.core import serializers
from django.http import HttpResponse
from sisred_app.models import ProyectoRED, Recurso, RED


def getProyectosRED(request):
    vLstObjects = list(ProyectoRED.objects.all())
    return HttpResponse(serializers.serialize('json', vLstObjects), content_type="application/json")

def getRecurso(request):
    vLstObjects = list(Recurso.objects.all())
    return HttpResponse(serializers.serialize('json', vLstObjects), content_type="application/json")

def getRED(request):
    vLstObjects = list(RED.objects.all())
    return HttpResponse(serializers.serialize('json', vLstObjects), content_type="application/json")
