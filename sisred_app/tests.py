from django.test import TestCase
from django.contrib.auth.models import User
from .models import RED, Version, ProyectoConectate, Perfil, Recurso
import json
# Create your tests here.

class VersionTestCase(TestCase):


    def test_get_info_version(self):
        user = User.objects.create_user(username='test', password='123456', email='test@test.com', first_name='test',
                                        last_name='T')
        perfil = Perfil.objects.create(id_conectate=123, usuario=user, estado=1)
        proyecto = ProyectoConectate.objects.create(id_conectate='1', nombre='MISO', codigo='1234',
                                                    fecha_inicio='2019-03-20', fecha_fin='2019-04-10')
        self.red = RED.objects.create(id_conectate='1', nombre='elRED', descripcion=' ',
                                      tipo='video', solicitante='', proyecto_conectate=proyecto)
        self.version = Version.objects.create(numero=1, red=self.red, creadoPor=perfil, fecha_creacion='2019-03-20',
                                              imagen='https://i.pinimg.com/736x/3e/63/03/3e630381b8e25dda523301dc800c8c1d.jpg')

        url = '/api/versiones/'+str(self.version.pk)+'/'
        response = self.client.get(url)
        current_data = json.loads(response.content)
        self.assertEqual(current_data['numero'], 1)

    def test_get_info_version2(self):
        user = User.objects.create_user(username='test', password='123456', email='test@test.com', first_name='test',
                                        last_name='T')
        perfil = Perfil.objects.create(id_conectate=123, usuario=user, estado=1)
        proyecto = ProyectoConectate.objects.create(id_conectate='1', nombre='MISO', codigo='1234',
                                                    fecha_inicio='2019-03-20', fecha_fin='2019-04-10')
        self.red = RED.objects.create(id_conectate='1', nombre='elRED', descripcion=' ',
                                      tipo='video', solicitante='', proyecto_conectate=proyecto)
        self.version = Version.objects.create(numero=1, red=self.red, creadoPor=perfil, fecha_creacion='2019-03-20',
                                              imagen='https://i.pinimg.com/736x/3e/63/03/3e630381b8e25dda523301dc800c8c1d.jpg')
        self.version2 = Version.objects.create(numero=2, red=self.red, creadoPor=perfil, fecha_creacion='2019-03-20',
                                              imagen='https://i.pinimg.com/736x/3e/63/03/3e630381b8e25dda523301dc800c8c1d.jpg')

        url = '/api/versiones/' + str(self.version2.pk) + '/'
        response = self.client.get(url)
        current_data = json.loads(response.content)
        self.assertEqual(current_data['numero'], 2)

    def test_get_info_version3(self):
        user = User.objects.create_user(username='test', password='123456', email='test@test.com', first_name='test',
                                        last_name='T')
        perfil = Perfil.objects.create(id_conectate=123, usuario=user, estado=1)
        proyecto = ProyectoConectate.objects.create(id_conectate='1', nombre='MISO', codigo='1234',
                                                    fecha_inicio='2019-03-20', fecha_fin='2019-04-10')
        self.red = RED.objects.create(id_conectate='1', nombre='elRED', descripcion=' ',
                                      tipo='video', solicitante='', proyecto_conectate=proyecto)
        self.version = Version.objects.create(numero=1, red=self.red, creadoPor=perfil, fecha_creacion='2019-03-20',
                                              imagen='https://i.pinimg.com/736x/3e/63/03/3e630381b8e25dda523301dc800c8c1d.jpg')

        url = '/api/versiones/' + str(self.version.pk) + '/'
        response = self.client.get(url)
        current_data = json.loads(response.content)
        self.assertEqual(current_data['numero'], 1)
        self.assertEqual(current_data['red']['proyecto_conectate']['nombre'],'MISO')

    def test_get_recursos_version(self):
        user = User.objects.create_user(username='test', password='123456', email='test@test.com', first_name='test',
                                        last_name='T')
        perfil = Perfil.objects.create(id_conectate=123, usuario=user, estado=1)
        proyecto = ProyectoConectate.objects.create(id_conectate='1', nombre='MISO', codigo='1234',
                                                    fecha_inicio='2019-03-20', fecha_fin='2019-04-10')
        recurso1 = Recurso.objects.create(nombre='test', tipo ='PNG', archivo='url', thumbnail='url1', descripcion=' ', autor=perfil, usuario_ultima_modificacion=perfil)
        recurso2 = Recurso.objects.create(nombre='test2', tipo ='AVI', archivo='url2', thumbnail='url3', descripcion=' ', autor=perfil, usuario_ultima_modificacion=perfil)

        self.red = RED.objects.create(id_conectate='1', nombre='elRED', descripcion=' ',
                                      tipo='video', solicitante='', proyecto_conectate=proyecto)
        self.version = Version.objects.create(numero=1, red=self.red, creadoPor=perfil, fecha_creacion='2019-03-20',
                                              imagen='https://i.pinimg.com/736x/3e/63/03/3e630381b8e25dda523301dc800c8c1d.jpg')

        self.version.recursos.set([recurso1,recurso2])

        url = '/api/versiones/' + str(self.version.pk) + '/recursos/'
        response = self.client.get(url)
        current_data = json.loads(response.content)
        self.assertEqual(len(current_data['context']), 2)

    def test_get_recursos_version1(self):
        user = User.objects.create_user(username='test', password='123456', email='test@test.com', first_name='test',
                                        last_name='T')
        perfil = Perfil.objects.create(id_conectate=123, usuario=user, estado=1)
        proyecto = ProyectoConectate.objects.create(id_conectate='1', nombre='MISO', codigo='1234',
                                                    fecha_inicio='2019-03-20', fecha_fin='2019-04-10')
        recurso1 = Recurso.objects.create(nombre='test', tipo ='PNG', archivo='url', thumbnail='url1', descripcion=' ', autor=perfil, usuario_ultima_modificacion=perfil)
        recurso2 = Recurso.objects.create(nombre='test2', tipo ='AVI', archivo='url2', thumbnail='url3', descripcion=' ', autor=perfil, usuario_ultima_modificacion=perfil)

        self.red = RED.objects.create(id_conectate='1', nombre='elRED', descripcion=' ',
                                      tipo='video', solicitante='', proyecto_conectate=proyecto)
        self.version = Version.objects.create(numero=1, red=self.red, creadoPor=perfil, fecha_creacion='2019-03-20',
                                              imagen='https://i.pinimg.com/736x/3e/63/03/3e630381b8e25dda523301dc800c8c1d.jpg')

        self.version.recursos.set([recurso1,recurso2])

        url = '/api/versiones/' + str(self.version.pk) + '/recursos/'
        response = self.client.get(url)
        current_data = json.loads(response.content)
        self.assertEqual(current_data['context'][0]['nombre'], 'test')
        self.assertEqual(current_data['context'][1]['nombre'], 'test2')
        self.assertEqual(current_data['context'][0]['tipo'], 'PNG')
        self.assertEqual(current_data['context'][1]['tipo'], 'AVI')



