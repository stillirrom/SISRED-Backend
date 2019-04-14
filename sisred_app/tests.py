from django.test import TestCase
from sisred_app.models import User, Perfil

import json
from django.contrib import auth

# Create your tests here.

class loginTestCase(TestCase):
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
