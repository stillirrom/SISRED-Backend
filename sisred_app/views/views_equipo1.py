from django.contrib.auth.models import User
from django.db.models.query import QuerySet
from rest_framework import  status
from rest_framework.decorators import api_view
from rest_framework.exceptions import NotFound

from rest_framework.response import Response
import datetime


from sisred_app.models import Recurso, RED, Perfil, Version, Comentario, ComentarioMultimedia, ComentarioPDF
from sisred_app.serializer import RecursoSerializer, RecursoSerializer_put, \
    REDSerializer




#Autor: Francisco Perneth
#Fecha: 2019-03-30
#Parametros:
#    Request -> Datos de la solicitud
#Descripcion:
#   Permite registrar un recurso
@api_view(['POST'])
def recurso_post(request):
    autor = Perfil.objects.get(id=int(request.data.get("autor")))
    idRed = request.data.get("idRed")
    rec = Recurso.objects.create(nombre=request.data.get('nombre'),
                                     archivo=request.data.get('archivo'),
                                     thumbnail=request.data.get('thumbnail'),
                                     descripcion=request.data.get('descripcion'),
                                     tipo=request.data.get('tipo'),
                                     autor=autor,
                                     usuario_ultima_modificacion=autor
                                     )
    rec.fecha_creacion=datetime.datetime.now()
    rec.fecha_ultima_modificacion = datetime.datetime.now()
    rec.save()
    IdRecurso=rec.id

    Red=RED.objects.get(id=idRed)
    if (Red!=None):
        Red.recursos.add(rec)
        return Response(request.data, status=status.HTTP_201_CREATED)

#Autor: Francisco Perneth
#Fecha: 2019-03-30
#Parametros:
#    Request -> Datos de la solicitud
#    id -> id del recurso para obtener
#Descripcion:
#   Permite consultar un recurso mediante su identificador (id)
@api_view(['GET'])
def recurso_get(request,id):
    recurso = Recurso.objects.filter(id=id).first()
    if(recurso==None):
        raise NotFound(detail="Error 404, recurso not found", code=404)
    serializer = RecursoSerializer(recurso)
    return Response(serializer.data)

#Autor: Francisco Perneth
#Fecha: 2019-03-30
#Parametros:
#    Request -> Datos de la solicitud
#Descripcion:
#   Permite modificar un recurso mediante.
#   los datos permitios a modificar son: nombre y descripción. la fecha y usaurio de la modificación son valores tomados de
#   el usuario que está realizando la operación (auntenticado en el sistema) y la fecha del sistema.
@api_view(['PUT'])
def recurso_put(request):
    serializer = RecursoSerializer_put(data=request.data)
    if serializer.is_valid():
        id=int(request.data.get("id"))
        ItemRecurso = Recurso.objects.filter(id=id).first()
        if (ItemRecurso==None):
            raise NotFound(detail="Error 404, recurso not found", code=404)
        ItemRecurso.nombre=request.data.get("nombre")
        ItemRecurso.descripcion=request.data.get("descripcion")
        Per=Perfil.objects.get(id=int(request.data.get("usuario_ultima_modificacion")))
        if (Per!=None):
            ItemRecurso.usuario_ultima_modificacion=Per
        ItemRecurso.fecha_ultima_modificacion=datetime.datetime.now()
        ItemRecurso.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

#Autor: Ramiro Vargas
#Fecha: 2019-03-30
#Parametros:
#    Request -> Datos de la solicitud
#    id -> id del recurso para consultar
#Descripcion:
#   Permite consultar  la información de un RED, especialmente información del avance
@api_view(['GET', 'POST'])
def fase_byid(request,id):
    if request.method == 'GET':
        red = RED.objects.filter(id=id)
        if (red == None):
            raise NotFound(detail="Error 404, recurso not found", code=404)
        print(red)
        serializer = REDSerializer(red, many=True)
        return Response(serializer.data)


#Autor:         Adriana Vargas
#Fecha:         2019-04-11
#Parametros:    request -> Datos de la solicitud
#               numero_identificacion -> número de identificación del usuario
#Descripcion:   Permite consultar la información de un usuario con su número de identificación y actualizar el estado del mismo en sisred

@api_view(['GET', 'PUT'])
def getUserByIdentification(request, numero_identificacion):
    usuario_perfil = []

    try:
        perfil = Perfil.objects.get(numero_identificacion=numero_identificacion)
    except Perfil.DoesNotExist:
        raise NotFound(detail="Error 404, User not found", code=404)

    usuario = User.objects.get(username=perfil.usuario)

    if request.method == 'GET':

        usuario_perfil.append({"username": usuario.username, "email": usuario.email,
                               "first_name": usuario.first_name, "lastname": usuario.last_name,
                               "numero_identificacion": perfil.numero_identificacion,
                               "estado": perfil.estado, "estado_sisred": perfil.estado_sisred})

        return Response(usuario_perfil)

    elif request.method == 'PUT':

        perfil.estado_sisred = 1
        perfil.save()

        usuario_perfil.append({"username": usuario.username, "email": usuario.email,
                               "first_name": usuario.first_name, "lastname": usuario.last_name,
                               "numero_identificacion": perfil.numero_identificacion,
                               "estado": perfil.estado, "estado_sisred": perfil.estado_sisred})

        return Response(usuario_perfil)

@api_view(['GET', 'PUT'])
def getREDByIdentification(request, id_conectate):
    reds=[]
    try:
        red = RED.objects.get(id_conectate=id_conectate)
    except RED.DoesNotExist:
        raise NotFound(detail="Error 404, User not found", code=404)

    if request.method == 'GET':
        serializer = REDSerializer(red, many=True)
        return Response(serializer.data)

    elif request.method == 'PUT':

        red.listo=True
        red.save()
        reds.append({"nombre": red.nombre, "nombre_corto": red.nombre_corto,
                    "descripcion": red.descripcion, "fecha_inicio": red.fecha_inicio,
                    "fecha_cierre": red.fecha_cierre,
                    "fecha_creacion": red.fecha_creacion, "porcentaje_avance": red.porcentaje_avance,
                    "tipo": red.tipo, "solicitante": red.solicitante,
                    "horas_estimadas": red.horas_estimadas, "horas_trabajadas": red.horas_trabajadas,
                    "proyecto_conectate_id": red.proyecto_conectate_id,
                    "listo": True})
        return Response(reds)

#Autor:         Alejandro Garcia
#Fecha:         2019-04-17
#Parametros:    request -> Datos de la solicitud
#               id -> id del recurso comentado
#Descripcion:   Permite consultar los comentarios de una veersion de un RED y crear comentarios nuevos
@api_view(['GET'])
def getComentariosPDF(request, id):
    if request.method == 'GET':
        response = []
        try:
            recurso = Recurso.objects.get(pk=id)
            comentarios = Comentario.objects.filter(recurso=recurso)
            rutaPdf = {recurso.archivo}
            comentarios_multimedia = []

            for comentario in comentarios:
                comentarios_multimedia.append(ComentarioMultimedia.objects.filter(comentario=comentario))

            for com_multimedia in comentarios_multimedia:
                comentarios_PDF=ComentarioPDF.objects.filter(comentarios_multimedia=comentarios_multimedia)
                for comentario_PDF in comentarios_PDF:
                    coordenadas = {"height": comentario_PDF.height,
                                   "width": comentario_PDF.width,
                                   "x1": com_multimedia.x1,
                                   "y1": com_multimedia.y1,
                                   "x2": com_multimedia.x2,
                                   "y2": com_multimedia.y2}

                    c = Comentario.objects.get(pk=com_multimedia.comentario)
                    response.append({"rutaPdf": rutaPdf, "coordenadas": coordenadas, "comentarios": [c.contenido]})
            return response;
        except Exception as ex:
            raise NotFound(detail="Error 404, User not found", code=404)

@api_view(['POST'])
def postComentariosPDF(request):
    if request.method == 'POST':
        print("Persistiendo Comentarios PDF en BD")
        coordenadas = request.data.get("coordenadas")
        contenido = request.data.get("comentario")
        usuario = Perfil.objects.get(id=int(request.data.get("usuario")))
        version = Version.objects.get(id=int(request.data.get("version")))
        recurso = Recurso.objects.get(pk=int(request.data.get("recurso")))
        comment = Comentario.objects.create(usuario=usuario, version=version, recurso=recurso,  contenido=contenido)
        comment.save()
        mul_comment = ComentarioMultimedia.objects.create(x1=coordenadas['x1'], x2=coordenadas['x2'], y1=coordenadas['y1'], y2=coordenadas['y2'], comentario=comment)
        mul_comment.save()
        pdf_comment = ComentarioPDF.objects.create(height=coordenadas['height'],width=coordenadas['width'], comentario_multimedia=mul_comment)
        pdf_comment.save()
