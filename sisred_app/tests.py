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
        recurso = Recurso.objects.create(nombre='Recurso1', archivo='archivo1', thumbnail='thumbnail1',
                                         fecha_creacion='2019-04-25',
                                         fecha_ultima_modificacion='2019-04-25', tipo='jpg',
                                         descripcion='descripcion1', autor=perfil, usuario_ultima_modificacion=perfil)

        buscarNombre = "Recurso1"

        url = '/api/buscarRecurso/?name={buscarNombre}/'

        response =  self.client.get(url, format='json')

        self.assertEqual(response.status_code, 200)


