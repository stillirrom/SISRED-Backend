from django.test import TestCase
from .models import Version, RED, ProyectoConectate, Metadata, Perfil, Recurso, RolAsignado, Rol, ComentarioMultimedia, \
    Comentario
from django.contrib.auth.models import User
import datetime
import json
from django.forms.models import model_to_dict
from sisred_app.views.views_equipo4 import createNotification
from .models import User, Perfil, RED, Fase, ProyectoConectate, Recurso, NotificacionTipo, Rol, RolAsignado, \
    Notificacion
from django.contrib.auth.models import User
import json


# Create your tests here.

class sisred_appTestCase(TestCase):

    # Test Francisco Perneth
    #EndPoint ComentariosPDF
    def test_ComentariosPDF(self):
        user = User.objects.create_user(username='user', password='123456', email='user@user.com',first_name='User test',last_name='User ape')
        perfil = Perfil.objects.create(id_conectate=1, usuario=user, estado=1, estado_sisred=1)
        proyecto = ProyectoConectate.objects.create(id_conectate='1', nombre='Project Test', codigo='1234',fecha_inicio='2019-03-20', fecha_fin='2019-04-10')
        self.red = RED.objects.create(id_conectate='1', nombre='Test Red', descripcion=' ',tipo='image', solicitante='Test', proyecto_conectate=proyecto)
        self.version = Version.objects.create(numero=1, red=self.red, creado_por=perfil, fecha_creacion='2019-03-20',imagen='https://i.pinimg.com/736x/3e/63/03/3e630381b8e25dda523301dc800c8c1d.jpg')
        com_mul = ComentarioMultimedia.objects.create(x1=1, y1=5, x2=3, y2=5)
        comentario = Comentario.objects.create(contenido='Comentario test', version=self.version,usuario=perfil, comentario_multimedia=com_mul, esCierre=False,resuelto=False)
        comentario2 = Comentario.objects.create(contenido='Comentario base de prueba 2', version=self.version,usuario=perfil, comentario_multimedia=com_mul, esCierre=False,resuelto=False)
        response = self.client.get('/api/ComentariosPDF/' + str(comentario.id) + '/')
        current_data = json.loads(response.content)

        self.assertEqual(current_data[0]['contenido'], 'Comentario test')