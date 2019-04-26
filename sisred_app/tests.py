from django.test import TestCase
from .models import User, Perfil, RED, Fase, ProyectoConectate, Recurso
from django.contrib.auth.models import User
import json


# Create your tests here.
class BuscarRecursoTestCase(TestCase):

    def test_buscar_recurso_byName_status(self):
        user = User.objects.create(username='user1', password='1234ABC', first_name='nombre1',
                                   last_name='apellido1', email='user@uniandes.edu.co')
        perfil = Perfil.objects.create(id_conectate='1', usuario=user, tipo_identificacion='CC',
                                       numero_identificacion='1234', estado=1)
        recurso = Recurso.objects.create(nombre='Recurso5', archivo='archivo1', thumbnail='thumbnail1',
                                         fecha_creacion='2019-04-25',
                                         fecha_ultima_modificacion='2019-04-25', tipo='jpg',
                                         descripcion='descripcion1', autor=perfil, usuario_ultima_modificacion=perfil)

        buscarNombre = "Recurso5"

        url = f'/api/buscarRecurso/?name={buscarNombre}'

        response =  self.client.get(url, format='json')

        self.assertEqual(response.status_code, 200)


    def test_buscar_recurso_byFechaCreacion(self):
        user = User.objects.create(username='user1', password='1234ABC', first_name='nombre1',
                                   last_name='apellido1', email='user@uniandes.edu.co')
        perfil = Perfil.objects.create(id_conectate='1', usuario=user, tipo_identificacion='CC',
                                       numero_identificacion='1234', estado=1)
        Recurso.objects.create(nombre='Recurso1', archivo='archivo1', thumbnail='thumbnail1',
                                         fecha_creacion='2019-01-25',
                                         fecha_ultima_modificacion='2019-01-25', tipo='jpg',
                                         descripcion='descripcion1', autor=perfil, usuario_ultima_modificacion=perfil)
        Recurso.objects.create(nombre='Recurso2', archivo='archivo2', thumbnail='thumbnail1',
                                         fecha_creacion='2019-02-25',
                                         fecha_ultima_modificacion='2019-02-25', tipo='jpg',
                                         descripcion='descripcion2', autor=perfil, usuario_ultima_modificacion=perfil)
        Recurso.objects.create(nombre='Recurso3', archivo='archivo3', thumbnail='thumbnail1',
                                          fecha_creacion='2019-03-25',
                                          fecha_ultima_modificacion='2019-03-25', tipo='jpg',
                                          descripcion='descripcion3', autor=perfil, usuario_ultima_modificacion=perfil)

        buscarNombre = ""
        fecha_desde = "2019-01-01"
        fecha_hasta = "2019-02-28"

        url = f'/api/buscarRecurso/?name={buscarNombre}&fdesde={fecha_desde}&fhasta={fecha_hasta}'

        response = self.client.get(url, format='json')
        recursos = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(recursos), 2)


