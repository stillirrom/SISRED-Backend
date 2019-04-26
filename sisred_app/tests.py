from django.test import TestCase
from .models import User, Perfil, RED, Fase, ProyectoConectate, Recurso, NotificacionTipo, Rol, RolAsignado, \
    Notificacion
from django.contrib.auth.models import User
import json


# Create your tests here.
class sisRedTestCase(TestCase):

    def test_login(self):
        username = "gl.pinto10@uniandes.edu.co"
        first_name = "first_name"
        last_name = "last_name"
        password = "Test12345"
        id_conectate = "1"
        numero_identificacion = "123455"
        user_model = User.objects.create_user(username=username, password=password, first_name=first_name,
                                              last_name=last_name, email=username)
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
        response = self.client.put(
            '/api/red/' + str(red.id_conectate) + '/cambiarfase/' + str(fase2.id_conectate) + '/',
            content_type='application/json')

        print("response", response.status_code)
        self.assertEqual(response.status_code, 200)


    def test_list_fases(self):
        url = '/api/fases/'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, 200)


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


    def test_add_metadata_existente_recurso(self):
        user = User.objects.create(username='user1', password='1234ABC', first_name='nombre1',
                                   last_name='apellido1', email='user@uniandes.edu.co')
        perfil = Perfil.objects.create(id_conectate='1', usuario=user, tipo_identificacion='CC',
                                       numero_identificacion='1234', estado=1)
        recurso = Recurso.objects.create(nombre='Recurso1', archivo='archivo1', thumbnail='thumbnail1',
                                         fecha_creacion='2019-04-11',
                                         fecha_ultima_modificacion='2019-04-11', tipo='jpg',
                                         descripcion='descripcion1', autor=perfil, usuario_ultima_modificacion=perfil)

        url = '/api/addMetadataRecurso/' + str(recurso.id) + '/'

        self.client.post(url, json.dumps(
            {"tag": "metadata1"}), content_type='application/json')

        self.client.post(url, json.dumps(
            {"tag": "metadata1"}), content_type='application/json')

        recursoFiltrado = Recurso.objects.filter(pk=recurso.id).first()

        self.assertEqual((recursoFiltrado.metadata).count(), 1)

    def test_list_notificaciones_un_usuario(self):
        user = User.objects.create(username='user1', password='1234ABC', first_name='nombre1',
                                   last_name='apellido1', email='user@uniandes.edu.co')
        perfil = Perfil.objects.create(id_conectate=1, usuario=user, numero_identificacion='123',
                                       tipo_identificacion='CC', estado='1')
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
        rol = Rol.objects.create(id_conectate=1, nombre='Productor')
        tipoNotificacion = NotificacionTipo.objects.create(nombre='ASIGNAR_RED', descripcion='El red fue asignado.')
        notificacion = Notificacion.objects.create(mensaje='prueba', fecha='2019-01-26', visto=False,
                                                   tipo_notificacion=tipoNotificacion)

        rolAsignado = RolAsignado.objects.create(id_conectate=1, estado=1, red=red, rol=rol, usuario=perfil)
        rolAsignado.notificaciones.add(notificacion)
        url = '/api/notificaciones/' + str(perfil.id_conectate) + '/'

        response = self.client.get(url, format='json')
        current_data = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(current_data), 1)

    def test_numero_notificaciones_no_vistas(self):
        user = User.objects.create(username='user1', password='1234ABC', first_name='nombre1',
                                   last_name='apellido1', email='user@uniandes.edu.co')
        perfil = Perfil.objects.create(id_conectate=1,usuario=user,numero_identificacion='123',tipo_identificacion='CC',estado='1')
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
        rol = Rol.objects.create(id_conectate=1, nombre='Productor')
        tipoNotificacion = NotificacionTipo.objects.create(nombre='ASIGNAR_RED',descripcion='El red fue asignado.')
        notificacion = Notificacion.objects.create(mensaje='prueba',fecha='2019-01-26',visto=False,tipo_notificacion=tipoNotificacion)
        notificacion2 = Notificacion.objects.create(mensaje='prueba2',fecha='2019-01-26',visto=True,tipo_notificacion=tipoNotificacion)

        rolAsignado = RolAsignado.objects.create(id_conectate=1,estado=1,red=red,rol=rol,usuario=perfil)
        rolAsignado.notificaciones.add(notificacion)
        rolAsignado.notificaciones.add(notificacion2)
        url = '/api/notificaciones/' + str(perfil.id_conectate) + '/novistos/'

        response = self.client.get(url, format='json')
        current_data = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(current_data, 1)
