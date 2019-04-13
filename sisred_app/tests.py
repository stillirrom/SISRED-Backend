from django.test import TestCase
from datetime import datetime
from .models import RED, ProyectoConectate, Version, Perfil
from django.contrib.auth.models import User
import json
# Create your tests here.


class RR02TestCase(TestCase):

    def test_get_version(self):
        url = '/api/get_version/'
        fecha_inicio = datetime.strptime("2018-03-11", "%Y-%m-%d").date()
        fecha_fin = datetime.strptime("2018-03-11", "%Y-%m-%d").date()
        proyectto_conectate = ProyectoConectate.objects.create(id_conectate='1', nombre='prueba',
                                                               codigo='prueba', fecha_inicio=fecha_inicio,
                                                               fecha_fin=fecha_fin)
        red = RED.objects.create(id_conectate='1', nombre='pruebaRED', descripcion='prueba',
                                 tipo='prueba', solicitante='prueba', proyecto_conectate=proyectto_conectate)
        version = Version.objects.create(numero=1, imagen='prueba', red=red, id=1)
        response = self.client.get(url, {'id': '1'})
        current_data = json.loads(response.content)
        self.assertEqual(current_data[0]['fields']['nombre'], 'pruebaRED')
        self.assertEqual(current_data[1]['fields']['numero'], 1)

    def test_get_recursos(self):
        url = '/api/get_recursos_by_version/'
        fecha_inicio = datetime.strptime("2018-03-11", "%Y-%m-%d").date()
        fecha_fin = datetime.strptime("2018-03-11", "%Y-%m-%d").date()
        proyectto_conectate = ProyectoConectate.objects.create(id_conectate='1', nombre='prueba',
                                                               codigo='prueba', fecha_inicio=fecha_inicio,
                                                               fecha_fin=fecha_fin)
        red = RED.objects.create(id_conectate='1', nombre='pruebaRED', descripcion='prueba',
                                 tipo='prueba', solicitante='prueba', proyecto_conectate=proyectto_conectate)
        version = Version.objects.create(numero=1, imagen='prueba', red=red, id=1)
        user_model = User.objects.create_user(username='user1', password='1234ABC*', first_name='Usuario',
                                              last_name='uno', email='user1@coquito.com')
        perfil = Perfil.objects.create(id_conectate='1', usuario = user_model, estado=1)
        recurso = version.recursos.create(nombre='prueba', archivo='prueba', thumbnail='prueba', fecha_creacion=fecha_inicio,
                                          fecha_ultima_modificacion=fecha_inicio, tipo='prueba', descripcion='prueba',
                                          autor=perfil, usuario_ultima_modificacion=perfil)
        response = self.client.get(url, {'id': '1'})
        current_data = json.loads(response.content)
        self.assertEqual(len(current_data), 1)


