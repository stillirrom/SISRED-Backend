from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json
from .models import RED, ProyectoRED
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
