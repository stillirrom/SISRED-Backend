from django.core.serializers import json
from django.test import TestCase

# Create your tests here.
from sisred_app.models import RED, Fase, ProyectoConectate


class sisRedTestCase(TestCase):

    def test_cambiar_fase(self):

        print("test_cambiar_fase")
        proyecto_conectate = ProyectoConectate.objects.create(id_conectate='2', nombre='namepy',
                                                              nombre_corto='nameShort',
                                                              codigo='code', fecha_inicio='1999-12-19',
                                                              fecha_fin='2001-12-20')
        fase = Fase.objects.create(
            id_conectate='2',
            nombre_fase='produccion',
        )

        red = RED.objects.create(
            id_conectate='1',
            nombre='nombre',
            nombre_corto='nombre_corto',
            descripcion='descripcion',
            fecha_inicio=None,
            fecha_cierre=None,
            porcentaje_avance=50,
            tipo='tipo',
            solicitante='solicitante',
            proyecto_conectate=proyecto_conectate,
            horas_estimadas=8,
            horas_trabajadas=7,
            fase=fase,
        );

        fase2 = Fase.objects.create(
            id_conectate='3',
            nombre_fase='preproduccion',
        )

        response = self.client.put('/api/red/' + str(red.id_conectate) + '/cambiarfase/' + str(fase2.id_conectate) + '/',
                               content_type='application/json')

        print("response",response.status_code)
        self.assertEqual(response.status_code, 200)

