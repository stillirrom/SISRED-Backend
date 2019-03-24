from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json

from .models import RED, ProyectoRED, RolAsignado, Perfil
from django.http import HttpResponse
from django.core import serializers
# Create your views here.


@csrf_exempt
def post_proyecto_red(request):
    if request.method == 'POST':
        json_proyecto_red = json.loads(request.body)
        red = RED.objects.get(id=json_proyecto_red['RED'])
        nuevo_proyecto_red = ProyectoRED(
            nombre=json_proyecto_red['nombre'],
            tipo=json_proyecto_red['tipo'],
            carpeta=json_proyecto_red['carpeta'],
            red=red)
        nuevo_proyecto_red.save()
        return HttpResponse(serializers.serialize("json", [nuevo_proyecto_red]))


@csrf_exempt
def get_detailred_personas(request):
    if request.method == 'GET':
        json_info = json.loads(request.body)
        personas = RolAsignado.objects.filter(red=json_info['RED'])
        respuesta = []
        for persona in personas:
            nombre = persona.perfil.usuario.name
            rol = persona.rol
            respuesta.append({"nombre":nombre, "rol": rol})
        return HttpResponse(serializers.serialize("json", respuesta))


@csrf_exempt
def get_detailred_proyectosred(request):
    if request.method == 'GET':
        json_info = json.loads(request.body)
        personas = RolAsignado.objects.filter(red=json_info['RED'])
        respuesta = []
        for persona in personas:
            nombre = persona.perfil.usuario.name
            rol = persona.rol
            respuesta.append({"nombre": nombre, "rol": rol})
        return HttpResponse(serializers.serialize("json", respuesta))


@csrf_exempt
def get_detailred_metadata(request):
    if request.method == 'GET':
        json_info = json.loads(request.body)
        personas = RolAsignado.objects.filter(red=json_info['RED'])
        respuesta = []
        for persona in personas:
            nombre = persona.perfil.usuario.name
            rol = persona.rol
            respuesta.append({"nombre":nombre, "rol": rol})
        return HttpResponse(serializers.serialize("json", respuesta))


@csrf_exempt
def get_detailred_recursos(request):
    if request.method == 'GET':
        json_info = json.loads(request.body)
        personas = RolAsignado.objects.filter(red=json_info['RED'])
        respuesta = []
        for persona in personas:
            nombre = persona.perfil.usuario.name
            rol = persona.rol
            respuesta.append({"nombre":nombre, "rol": rol})
        return HttpResponse(serializers.serialize("json", respuesta))


@csrf_exempt
def get_detailred(request):
    if request.method == 'GET':
        json_info = json.loads(request.body)
        personas = RolAsignado.objects.filter(red=json_info['RED'])
        respuesta = []
        for persona in personas:
            nombre = persona.perfil.usuario.name
            rol = persona.rol
            respuesta.append({"nombre":nombre, "rol": rol})
        return HttpResponse(serializers.serialize("json", respuesta))
