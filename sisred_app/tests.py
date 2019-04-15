from django.test import TestCase
from .models import Recurso, Perfil, Fase
from django.contrib.auth.models import User
import json


# Create your tests here.
class MetadadaRecursoTestCase(TestCase):

    def test_add_metadata_recurso_status(self):
        user = User.objects.create(username='user1', password='1234ABC', first_name='nombre1',
                                        last_name='apellido1', email='user@uniandes.edu.co')
        perfil = Perfil.objects.create(id_conectate='1', usuario=user, tipo_identificacion='CC',
                                        numero_identificacion='1234', estado=1)
        recurso = Recurso.objects.create(nombre='Recurso1', archivo='archivo1', thumbnail='thumbnail1',
                                                 fecha_creacion='2019-04-11',
                                                 fecha_ultima_modificacion='2019-04-11', tipo='jpg',
                                                 descripcion='descripcion1', autor=perfil, usuario_ultima_modificacion=perfil)

        url = '/api/addMetadataRecurso/' + str(recurso.id) + '/'

        response = self.client.post(url, json.dumps(
            {"tag": "metadata1"}), content_type='application/json')

        self.assertEqual(response.status_code, 200)
