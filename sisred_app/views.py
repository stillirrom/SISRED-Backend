from rest_framework import  status
from rest_framework.decorators import api_view
from rest_framework.exceptions import NotFound

from rest_framework.response import Response



from sisred_app.models import Recurso, RED
from sisred_app.serializer import RecursoSerializer, FaseSerializer


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
        if(recurso==None):
            raise NotFound(detail="Error 404, recurso not found", code=404)
        serializer = RecursoSerializer(recurso)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = RecursoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
@api_view(['GET', 'POST'])
def fase_byid(request,id):
    if request.method == 'GET':
        fase = RED.objects.filter(id=id).first()
        if(fase==None):
            raise NotFound(detail="Error 404, RED not found", code=404)
        serializer = FaseSerializer(fase)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = FaseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)