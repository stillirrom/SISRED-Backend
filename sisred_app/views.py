from django.shortcuts import render

from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.decorators import api_view, parser_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import FormParser, MultiPartParser


from sisred_app.models import Recurso, Estado
from sisred_app.serializer import RecursoSerializer ,EstadoSerializer
# Create your views here.


@api_view(['GET', 'POST'])
def recurso_list(request):
    if request.method == 'GET':
        recurso = Recurso.objects.all()
        serializer = RecursoSerializer(recurso, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = RecursoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
def recurso_addget(request,id):
    if request.method == 'GET':
        recurso = Recurso.objects.filter(id=id).first()
        serializer = RecursoSerializer(recurso)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = RecursoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
@api_view(['GET', 'POST'])
def estado_byid(request,id):
    if request.method == 'GET':
        recurso = Estado.objects.filter(id=id).first()
        serializer = EstadoSerializer(recurso)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = EstadoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)