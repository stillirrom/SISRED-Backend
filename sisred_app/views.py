from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json

from .models import RED, ProyectoRED, RolAsignado, Perfil, Metadata, Recurso, ProyectoConectate
from django.http import HttpResponse
from django.core import serializers
from django.contrib.auth.models import User
# Create your views here.


# Metodo para agregar un proyecto RED
@csrf_exempt
def post_proyecto_red(request):
    if request.method == 'POST':
        json_proyecto_red = json.loads(request.body)
        red = RED.objects.get(id=json_proyecto_red['RED'])
        nuevo_proyecto_red = ProyectoRED(
            nombre=json_proyecto_red['nombre'],
            tipo=json_proyecto_red['tipo'],
            carpeta=json_proyecto_red['carpeta'],
            descipcion=json_proyecto_red['descipcion'],
            autor=json_proyecto_red['autor'],
            red=red)
        nuevo_proyecto_red.save()
        return HttpResponse(serializers.serialize("json", [nuevo_proyecto_red]))


@csrf_exempt
def get_detallered_personas(request):
    if request.method == 'GET':
        red = RED.objects.get(nombre=request.GET['RED'])
        personas = RolAsignado.objects.filter(red=red)
        respuesta = []
        for persona in personas:
            nombre = persona.perfil.usuario.name
            rol = persona.rol
            respuesta.append({"nombre":nombre, "rol": rol})
        return HttpResponse(serializers.serialize("json", respuesta))


@csrf_exempt
def get_detallered_proyectosred(request):
    if request.method == 'GET':
        red = RED.objects.get(nombre=request.GET['RED'])
        respuesta = ProyectoRED.objects.filter(red=red)
        return HttpResponse(serializers.serialize("json", respuesta))


@csrf_exempt
def get_detallered_metadata(request):
    if request.method == 'GET':
        red = RED.objects.get(nombre=request.GET['RED'])
        respuesta = Metadata.objects.filter(red=red)
        return HttpResponse(serializers.serialize("json", respuesta))


@csrf_exempt
def get_detallered_recursos(request):
    if request.method == 'GET':
        red = RED.objects.get(nombre=request.GET['RED'])
        respuesta = Recurso.objects.filter(red=red)
        return HttpResponse(serializers.serialize("json", respuesta))


@csrf_exempt
def get_detallered(request):
    if request.method == 'GET':
        red = request.GET['RED']
        respuesta = RED.objects.get(nombre=red)
        return HttpResponse(serializers.serialize("json", [respuesta]))


@csrf_exempt
def create(request):
    user = User.objects.create_user(username='user', password='1234ABC', first_name='Usuario', last_name='Prueba',email='userpruerba@prueba.com')
    perfil = Perfil.objects.create(usuario=user, tipo_identificacion="Cedula", numero_identificacion="1111111111")
    metadata = Metadata.objects.create(tag="Prueba")
    proyecto = ProyectoConectate.objects.create()
    recurso1 = Recurso.objects.create(nombre="RecursoPrueba", archivo="pruebadearchivo", thumbnail="pruebathumbnail", tipo="tipoPrueba", descripcion="descripcion de prueba para este recurso de aca", autor=perfil, usuario_ultima_modificacion=perfil)
    red = RED.objects.create(codigo="PP", nombre="REDPrueba", nombre_corto="RedP", proyecto_conectate=proyecto)
    red.metadata.add(metadata)
    rol = RolAsignado.objects.create(usuario=perfil, red=red)
    red.metadata.add(metadata)
    return HttpResponse(serializers.serialize("json", [red]))

@csrf_exempt
def add(request):
    user = User.objects.create_user(username='user', password='1234ABC', first_name='Usuario', last_name='Prueba',email='userpruerba@prueba.com')
    perfil = Perfil.objects.create(usuario=user, tipo_identificacion="Cedula", numero_identificacion="1111111111")
    metadata = Metadata.objects.create(tag="Prueba")
    proyecto = ProyectoConectate.objects.create()
    recurso1 = Recurso.objects.create(nombre="RecursoPrueba", archivo="pruebadearchivo", thumbnail="pruebathumbnail", tipo="tipoPrueba", descripcion="descripcion de prueba para este recurso de aca", autor=perfil, usuario_ultima_modificacion=perfil)
    red = RED.objects.create(codigo="PP", nombre="REDPrueba", nombre_corto="RedP", proyecto_conectate=proyecto)
    red.metadata.add(metadata)
    rol = RolAsignado.objects.create(usuario=perfil, red=red)
    red.metadata.add(metadata)
    return HttpResponse(serializers.serialize("json", [red]))

@csrf_exempt
def get_reds_asignados(request, id):
    usuario = User.objects.get(pk=id);
    nombreUsuario = usuario.first_name + " " + usuario.last_name
    perfil = Perfil.objects.get(usuario=usuario);
    reds_asignados = []
    rolesAsignado = RolAsignado.objects.filter(usuario=perfil)
    for rolAsignado in rolesAsignado:
        red = rolAsignado.red
        rol = rolAsignado.rol.nombre
        reds_asignados.append({"idRed": red.pk, "nombreRed": red.nombre_corto, "rol": rol})
    respuesta = [{"nombreUsuario": nombreUsuario, "redsAsignados": reds_asignados}]
    return HttpResponse(respuesta)