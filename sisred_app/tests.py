from django.test import TestCase
from datetime import datetime
from .models import RED, ProyectoConectate, Version
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
        version = Version.objects.create(numero=1, archivo='prueba', red=red, id=1)
        response = self.client.get(url, {'id': '1'})
        current_data = json.loads(response.content)
        self.assertEqual(current_data[0]['fields']['nombre'], 'pruebaRED')
        self.assertEqual(current_data[1]['fields']['numero'], 1)


