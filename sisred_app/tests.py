from django.core.serializers import json
from django.test import TestCase
from sisred_app.models import User, Perfil, RED, Fase, ProyectoConectate

import json
from django.contrib import auth

# Create your tests here.

class sisRedTestCase(TestCase):
    def test_login(self):
        username = "gl.pinto10@uniandes.edu.co"
        first_name = "first_name"
        last_name = "last_name"
        password = "Test12345"
        id_conectate = "1"
        numero_identificacion = "123455"
        user_model = User.objects.create_user(username=username, password=password, first_name=first_name, last_name=last_name, email=username)
        user_profile = Perfil.objects.create(usuario=user_model, id_conectate=id_conectate,
                                             numero_identificacion=numero_identificacion, estado=1)
        user_profile.save()
        response = self.client.post('/api/login/', json.dumps({"username": username, "password": password}),
                                    content_type='application/json')
        current_data = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(current_data['token'])
        self.assertEqual(id_conectate, current_data['idConectate'])
        self.assertEqual(first_name, current_data['firstName'])
        self.assertEqual(last_name, current_data['lastName'])
        self.assertEqual(numero_identificacion, current_data['numeroIdentificacion'])

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


    def test_list_fases(self):
        url = '/api/fases/'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, 200)
