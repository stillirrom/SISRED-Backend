from django.core import serializers
from django.http import HttpResponse
import requests
from django.views.decorators.csrf import csrf_exempt
from sisred_app.models import ProyectoRED, Recurso, RED, ProyectoConectate, RolAsignado, Rol, Perfil, Estado, Fase, SubirRed



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

def getProyectoContectatePorId(request, id):
    vLstObjects = Fase.objects.filter(pk=id)
    return HttpResponse(serializers.serialize('json', vLstObjects), content_type="application/json")

def getRedDeProyectoContectatePorId(request, id):
    vLstObjects = Fase.objects.filter(pk=id)
    return HttpResponse(serializers.serialize('json', vLstObjects), content_type="application/json")

def subirRed(request):
    access_token = 'axrp2tiqri3l4yt'
    subirRed = SubirRed(access_token)

    enlaceSubida = subirRed.obtenerEnlaceSubida()

    data = open('', 'rb').read()
    res = requests.post(url=enlaceSubida, data=request.body, headers={'Content-Type': 'application/octet-stream'})
    if (res.status_code == 200):
        print("Success. Content hash: " + res.json()['content-hash'])
    elif (res.status_code == 409):
        print(
            "Conflict. The link does not exist or is currently unavailable, the upload failed, or another error happened.")
    elif (res.status_code == 410):
        print("Gone. The link is expired or already consumed.")
    else:
        print("Other error")

