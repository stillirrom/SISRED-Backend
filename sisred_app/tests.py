from django.test import TestCase
from sisred_app.models import User

import json
from django.contrib import auth

# Create your tests here.

class loginTestCase(TestCase):
    def test_login(self):
        username = "gl.pinto10@uniandes.edu.co"
        password = "Test12345"

        user = User(first_name="Test", last_name="Test", email=username, username=username, password=password)
        user.save()

        response = self.client.post('/api/login/', json.dumps({"username": username, "password": password}),
                                    content_type='application/json')
        current_data = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(current_data.token)
