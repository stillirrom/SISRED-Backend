from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseBadRequest
from django.core import serializers
from .models import User, Perfil
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.status import (
    HTTP_400_BAD_REQUEST
)
import json

from django.shortcuts import render

# Create your views here.

"""
Vista para crear un usuario nuevo (POST)
Parametros: request (en el body se agregan los atributos del modelo de User y perfil)
Return: El usuario creado con su id en formato Json
"""
@csrf_exempt
def add_user_view(request):
    if request.method == 'POST':
        try:
            json_user = json.loads(request.body)
            username = json_user['username']
            first_name = json_user['first_name']
            last_name = json_user['last_name']
            password = json_user['password']
            email = json_user['email']
            id_conectate=json_user['id_conectate']
            numero_identificacion=json_user['numero_identificacion']

            user_model = User.objects.create_user(username=username, password=password)
            user_model.first_name = first_name
            user_model.last_name = last_name
            user_model.email = email
            user_model.save()
            user_profile = Perfil.objects.create(usuario=user_model, id_conectate=id_conectate, numero_identificacion=numero_identificacion)
            user_profile.save()

            return HttpResponse(serializers.serialize("json", [user_model, user_profile]))
        except KeyError as e:
            return HttpResponseBadRequest(
                content='El campo ' + str(e) + ' es requerido.'
            )
        except Exception as ex:
            print('error')
            return HttpResponseBadRequest(
                content='BAD_REQUEST: ' + str(ex),
                status=HTTP_400_BAD_REQUEST
            )
"""
Vista para editar un usuario nuevo (PUT)
Parametros: request (en el body se agregan los atributos que se pueden modificar del modelo de User y perfil), id
Return: El usuario editado en formato Json
"""
@csrf_exempt
def update_user_view(request, id):
    if request.method == 'PUT':
        try:
            json_user = json.loads(request.body)
            first_name = json_user['first_name']
            last_name = json_user['last_name']
            email = json_user['email']
            id_conectate=json_user['id_conectate']
            numero_identificacion = json_user['numero_identificacion']

            user = User.objects.get(id=id)
            perfil = Perfil.objects.get(usuario=id)

            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            perfil.id_conectate = id_conectate
            perfil.numero_identificacion = numero_identificacion

            perfil.save()
            user.save()
            return HttpResponse(serializers.serialize("json",[user, perfil]))
        except ObjectDoesNotExist as e:
            return HttpResponseBadRequest(
                content='No existe el usuario con id ' + str(id)
            )
        except KeyError as e:
            return HttpResponseBadRequest(
                content='El campo ' + str(e) + ' es requerido.'
            )
        except Exception as ex:
            return HttpResponseBadRequest(
                content='BAD_REQUEST: ' + str(ex),
                status=HTTP_400_BAD_REQUEST
            )

"""
Vista para consultar todos los usuarios (GET)
Parametros: request
Return: Lista de los usuarios con sus perfiles en formato Json
"""
@csrf_exempt
def get_all_users(request):
    try:
        users = User.objects.filter(is_superuser=False)
        serialize = ""
        for user in users:
            perfil = Perfil.objects.get(usuario=user)
            serialize += serializers.serialize("json", [user, perfil])
        return HttpResponse(serialize)
    except Exception as ex:
        return HttpResponseBadRequest(
            content='BAD_REQUEST: ' + str(ex),
            status=HTTP_400_BAD_REQUEST
        )

"""
Vista para consultar el usuario por id (GET)
Parametros: request, id
Return: Usuario con su perfil en formato Json
"""
@csrf_exempt
def get_user_id_view(request, id):
    try:
        user = User.objects.get(id=id)
        perfil = Perfil.objects.get(usuario=user)
        return HttpResponse(serializers.serialize("json", [user, perfil]))
    except ObjectDoesNotExist as e:
        return HttpResponseBadRequest(
            content='No existe el usuario con id ' + str(id)
        )
    except Exception as ex:
        return HttpResponseBadRequest(
            content='BAD_REQUEST: ' + str(ex),
            status=HTTP_400_BAD_REQUEST
        )


