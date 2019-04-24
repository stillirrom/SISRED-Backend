from django.test import TestCase
from .models import Version, RED, ProyectoConectate, Metadata, Perfil, Recurso, RolAsignado, Rol
from django.contrib.auth.models import User
import datetime
import json

# Create your tests here.
class sisred_appTestCase(TestCase):

    def setUp(self):
        user = User.objects.create_user(username='test', password='sihdfnssejkhfse', email='test@test.com')
        self.perfil = Perfil.objects.create(id_conectate='1', usuario=user, estado=1)
        self.rol = Rol.objects.create(id_conectate='1', nombre='rolPrueba')

    def testMarcarComoVersionFinalJustOne(self):
        url1='/api/versiones/'
        url2='/marcar'
        versionId="1"
        url = url1+versionId+url2

        fecha = datetime.datetime.now()
        proyecto = ProyectoConectate.objects.create(id=1,fecha_inicio=fecha,fecha_fin=fecha)
        red = RED.objects.create(id=1, proyecto_conectate=proyecto)
        versionMain = Version.objects.create(id=1,es_final=False, numero=1, red=red)

        response =  self.client.post(url, format='json')

        versionMainAfter = Version.objects.get(id=1)

        self.assertEqual(response.status_code , 200)
        self.assertEqual(versionMainAfter.es_final,True)

    def testMarcarComoVersionFinalFirstMark(self):
        url1='/api/versiones/'
        url2='/marcar'
        versionId="2"
        url = url1+versionId+url2

        fecha = datetime.datetime.now()
        proyecto = ProyectoConectate.objects.create(id=1,fecha_inicio=fecha,fecha_fin=fecha)
        red = RED.objects.create(id=1, proyecto_conectate=proyecto)
        versionMain = Version.objects.create(id=2,es_final=False, numero=2, red=red)
        versionMain = Version.objects.create(id=1,es_final=False, numero=1, red=red)

        response =  self.client.post(url, format='json')

        versionMainAfter1 = Version.objects.get(id=1)
        versionMainAfter2 = Version.objects.get(id=2)

        self.assertEqual(response.status_code , 200)
        self.assertEqual(versionMainAfter1.es_final,False)
        self.assertEqual(versionMainAfter2.es_final,True)

    def testMarcarComoVersionFinalSecondMark(self):
        url1='/api/versiones/'
        url2='/marcar'
        versionId="2"
        url = url1+versionId+url2

        fecha = datetime.datetime.now()
        proyecto = ProyectoConectate.objects.create(id=1,fecha_inicio=fecha,fecha_fin=fecha)
        red = RED.objects.create(id=1, proyecto_conectate=proyecto)
        versionMain = Version.objects.create(id=2,es_final=False, numero=2, red=red)
        versionMain = Version.objects.create(id=1,es_final=True, numero=1, red=red)

        response =  self.client.post(url, format='json')

        versionMainAfter1 = Version.objects.get(id=1)
        versionMainAfter2 = Version.objects.get(id=2)

        self.assertEqual(response.status_code , 200)
        self.assertEqual(versionMainAfter1.es_final,False)
        self.assertEqual(versionMainAfter2.es_final,True)
    
    def testBuscarRedNameAllParameters(self):
        fecha = datetime.datetime.now()
        proyecto = ProyectoConectate.objects.create(id=3,fecha_inicio=fecha,fecha_fin=fecha)
        #RED.objects.create(id=, proyecto_conectate=proyecto, nombre="", nombre_corto="", descripcion=)
        red1 = RED.objects.create(id=1, id_conectate="1", proyecto_conectate=proyecto, nombre="video red", nombre_corto="vred", descripcion="descripcion de video", fecha_inicio=datetime.datetime.now(),fecha_cierre=datetime.datetime.now())
        red2 = RED.objects.create(id=2, id_conectate="2", proyecto_conectate=proyecto, nombre="sonido red", nombre_corto="sred", descripcion="descripcion de sonido", fecha_inicio=datetime.datetime.now(),fecha_cierre=datetime.datetime.now())
        RolAsignado.objects.create(id_conectate='1', estado=1, red=red1, rol=self.rol, usuario=self.perfil)
        RolAsignado.objects.create(id_conectate='2', estado=1, red=red2, rol=self.rol, usuario=self.perfil)
        buscarNombre = "video"
        fecha_inicio = "1987-12-28"
        fecha_fin = "3000-12-28"

        url = f"/api/buscarReds/{self.perfil.usuario.pk}/?text={buscarNombre}&fstart={fecha_inicio}&fend={fecha_fin}"

        response =  self.client.get(url, format='json')
        reds = json.loads(response.content)

        self.assertEqual(response.status_code , 200)
        self.assertEqual(len(reds), 1)    

    def testBuscarRedNameAllByNameNoDates(self):
        fecha = datetime.datetime.now()
        proyecto = ProyectoConectate.objects.create(id=3,fecha_inicio=fecha,fecha_fin=fecha)
        #RED.objects.create(id=, proyecto_conectate=proyecto, nombre="", nombre_corto="", descripcion=)
        red1 = RED.objects.create(id=1, id_conectate="1", proyecto_conectate=proyecto, nombre="video red", nombre_corto="vred", descripcion="descripcion de video", fecha_inicio=datetime.datetime.now(),fecha_cierre=datetime.datetime.now())
        red2 = RED.objects.create(id=2, id_conectate="2", proyecto_conectate=proyecto, nombre="sonido red", nombre_corto="sred", descripcion="descripcion de sonido", fecha_inicio=datetime.datetime.now(),fecha_cierre=datetime.datetime.now())
        RolAsignado.objects.create(id_conectate='1', estado=1, red=red1, rol=self.rol, usuario=self.perfil)
        RolAsignado.objects.create(id_conectate='2', estado=1, red=red2, rol=self.rol, usuario=self.perfil)
        buscarNombre = "video"

        url = f"/api/buscarReds/{self.perfil.usuario.pk}/?text={buscarNombre}"

        response =  self.client.get(url, format='json')
        reds = json.loads(response.content)

        self.assertEqual(response.status_code , 200)
        self.assertEqual(len(reds), 1)    

    def testBuscarRedNameByName(self):
        fecha = datetime.datetime.now()
        proyecto = ProyectoConectate.objects.create(id=3,fecha_inicio=fecha,fecha_fin=fecha)
        #RED.objects.create(id=, proyecto_conectate=proyecto, nombre="", nombre_corto="", descripcion=)
        red1 = RED.objects.create(id=1, id_conectate="1", proyecto_conectate=proyecto, nombre="video3 red", nombre_corto="vred", descripcion="descripcion de video", fecha_inicio=datetime.datetime.now(),fecha_cierre=datetime.datetime.now())
        red2 = RED.objects.create(id=2, id_conectate="2", proyecto_conectate=proyecto, nombre="sonido red", nombre_corto="sred", descripcion="descripcion de sonido", fecha_inicio=datetime.datetime.now(),fecha_cierre=datetime.datetime.now())
        RED.objects.create(id=3, id_conectate="3", proyecto_conectate=proyecto, nombre="video3 red", nombre_corto="sred", descripcion="descripcion de video", fecha_inicio=datetime.datetime.now(),fecha_cierre=datetime.datetime.now())

        RolAsignado.objects.create(id_conectate='1', estado=1, red=red1, rol=self.rol, usuario=self.perfil)
        RolAsignado.objects.create(id_conectate='2', estado=1, red=red2, rol=self.rol, usuario=self.perfil)

        buscarNombre = "video3"
        fecha_inicio = "1987-12-28"
        fecha_fin = "3000-12-28"

        url = f"/api/buscarReds/{self.perfil.usuario.pk}/?text={buscarNombre}&fstart={fecha_inicio}&fend={fecha_fin}"

        response =  self.client.get(url, format='json')
        reds = json.loads(response.content)
        self.assertEqual(response.status_code , 200)
        self.assertEqual(len(reds), 1)    
        self.assertEqual(reds[0]['id'], 1)  

    def testBuscarRedNameByshortName(self):
        fecha = datetime.datetime.now()
        proyecto = ProyectoConectate.objects.create(id=3,fecha_inicio=fecha,fecha_fin=fecha)
        #RED.objects.create(id=, proyecto_conectate=proyecto, nombre="", nombre_corto="", descripcion=)
        red1 = RED.objects.create(id=1, id_conectate="1", proyecto_conectate=proyecto, nombre="video3 red", nombre_corto="vred", descripcion="descripcion de video", fecha_inicio=datetime.datetime.now(),fecha_cierre=datetime.datetime.now())
        red2 = RED.objects.create(id=2, id_conectate="2", proyecto_conectate=proyecto, nombre="sonido red", nombre_corto="sred", descripcion="descripcion de sonido", fecha_inicio=datetime.datetime.now(),fecha_cierre=datetime.datetime.now())
        red3 = RED.objects.create(id=3, id_conectate="3", proyecto_conectate=proyecto, nombre="video3 red", nombre_corto="sred", descripcion="descripcion de video", fecha_inicio=datetime.datetime.now(),fecha_cierre=datetime.datetime.now())

        RolAsignado.objects.create(id_conectate='1', estado=1, red=red1, rol=self.rol, usuario=self.perfil)
        RolAsignado.objects.create(id_conectate='2', estado=1, red=red2, rol=self.rol, usuario=self.perfil)
        RolAsignado.objects.create(id_conectate='3', estado=1, red=red3, rol=self.rol, usuario=self.perfil)

        buscarNombre = "sred"
        fecha_inicio = "1987-12-28"
        fecha_fin = "3000-12-28"

        url = f"/api/buscarReds/{self.perfil.usuario.pk}/?text={buscarNombre}&fstart={fecha_inicio}&fend={fecha_fin}"

        response =  self.client.get(url, format='json')
        reds = json.loads(response.content)
        
        self.assertEqual(response.status_code , 200)
        self.assertEqual(len(reds), 2)    
        self.assertEqual(reds[0]['id'], 2)    
        self.assertEqual(reds[1]['id'], 3) 

    def testBuscarRedNameByDescription(self):
        fecha = datetime.datetime.now()
        proyecto = ProyectoConectate.objects.create(id=3,fecha_inicio=fecha,fecha_fin=fecha)
        #RED.objects.create(id=, proyecto_conectate=proyecto, nombre="", nombre_corto="", descripcion=)
        red1 = RED.objects.create(id=1, id_conectate="1", proyecto_conectate=proyecto, nombre="video3 red", nombre_corto="vred", descripcion="descripcion de video", fecha_inicio=datetime.datetime.now(),fecha_cierre=datetime.datetime.now())
        red2 = RED.objects.create(id=2, id_conectate="2", proyecto_conectate=proyecto, nombre="sonido red", nombre_corto="sred", descripcion="descripcion de sonido", fecha_inicio=datetime.datetime.now(),fecha_cierre=datetime.datetime.now())
        red3 = RED.objects.create(id=3, id_conectate="3", proyecto_conectate=proyecto, nombre="video3 red", nombre_corto="sred", descripcion="descripcion de video", fecha_inicio=datetime.datetime.now(),fecha_cierre=datetime.datetime.now())

        RolAsignado.objects.create(id_conectate='1', estado=1, red=red1, rol=self.rol, usuario=self.perfil)
        RolAsignado.objects.create(id_conectate='2', estado=1, red=red2, rol=self.rol, usuario=self.perfil)
        RolAsignado.objects.create(id_conectate='3', estado=1, red=red3, rol=self.rol, usuario=self.perfil)

        buscarNombre = "descripcion de video"
        fecha_inicio = "1987-12-28"
        fecha_fin = "3000-12-28"

        url = f"/api/buscarReds/{self.perfil.usuario.pk}/?text={buscarNombre}&fstart={fecha_inicio}&fend={fecha_fin}"

        response =  self.client.get(url, format='json')
        reds = json.loads(response.content)
        
        self.assertEqual(response.status_code , 200)
        self.assertEqual(len(reds), 2)    
        self.assertEqual(reds[0]['id'], 1)    
        self.assertEqual(reds[1]['id'], 3) 

    def testBuscarRedNameByTag(self):
        fecha = datetime.datetime.now()
        proyecto = ProyectoConectate.objects.create(id=3,fecha_inicio=fecha,fecha_fin=fecha)
        #RED.objects.create(id=, proyecto_conectate=proyecto, nombre="", nombre_corto="", descripcion=)
        red1 = RED.objects.create(id=1, id_conectate="1", proyecto_conectate=proyecto, nombre="video3 red", nombre_corto="vred", descripcion="descripcion de video", fecha_inicio=datetime.datetime.now(),fecha_cierre=datetime.datetime.now())
        red2 = RED.objects.create(id=2, id_conectate="2", proyecto_conectate=proyecto, nombre="sonido red", nombre_corto="sred", descripcion="descripcion de sonido", fecha_inicio=datetime.datetime.now(),fecha_cierre=datetime.datetime.now())
        red3 = RED.objects.create(id=3, id_conectate="3", proyecto_conectate=proyecto, nombre="video3 red", nombre_corto="sred", descripcion="descripcion de video", fecha_inicio=datetime.datetime.now(),fecha_cierre=datetime.datetime.now())

        RolAsignado.objects.create(id_conectate='1', estado=1, red=red1, rol=self.rol, usuario=self.perfil)
        RolAsignado.objects.create(id_conectate='2', estado=1, red=red2, rol=self.rol, usuario=self.perfil)
        RolAsignado.objects.create(id_conectate='3', estado=1, red=red3, rol=self.rol, usuario=self.perfil)

        tag = Metadata.objects.create(id = 1,tag="tag1")

        red1.metadata.add(tag)

        buscarNombre = "tag1"
        fecha_inicio = "1987-12-28"
        fecha_fin = "3000-12-28"

        url = f"/api/buscarReds/{self.perfil.usuario.pk}/?text={buscarNombre}&fstart={fecha_inicio}&fend={fecha_fin}"

        response =  self.client.get(url, format='json')
        reds = json.loads(response.content)
        
        self.assertEqual(response.status_code , 200)
        self.assertEqual(len(reds), 1)    
        self.assertEqual(reds[0]['id'], 1) 

    def testBuscarRedNameByAllText(self):
        fecha = datetime.datetime.now()
        proyecto = ProyectoConectate.objects.create(id=3,fecha_inicio=fecha,fecha_fin=fecha)

        red1 = RED.objects.create(id=1, id_conectate="1", proyecto_conectate=proyecto, nombre="test", nombre_corto="vred", descripcion="descripcion de video", fecha_inicio=datetime.datetime.now(),fecha_cierre=datetime.datetime.now())
        red2 = RED.objects.create(id=2, id_conectate="2", proyecto_conectate=proyecto, nombre="sonido red", nombre_corto="test", descripcion="descripcion de sonido", fecha_inicio=datetime.datetime.now(),fecha_cierre=datetime.datetime.now())
        red3 = RED.objects.create(id=3, id_conectate="3", proyecto_conectate=proyecto, nombre="video3 red", nombre_corto="sred", descripcion="descripcion de video", fecha_inicio=datetime.datetime.now(),fecha_cierre=datetime.datetime.now())
        red4 = RED.objects.create(id=4, id_conectate="4", proyecto_conectate=proyecto, nombre="video3 red", nombre_corto="sred", descripcion="descripcion test de video", fecha_inicio=datetime.datetime.now(),fecha_cierre=datetime.datetime.now())

        RolAsignado.objects.create(id_conectate='1', estado=1, red=red1, rol=self.rol, usuario=self.perfil)
        RolAsignado.objects.create(id_conectate='2', estado=1, red=red2, rol=self.rol, usuario=self.perfil)
        RolAsignado.objects.create(id_conectate='3', estado=1, red=red3, rol=self.rol, usuario=self.perfil)
        RolAsignado.objects.create(id_conectate='4', estado=1, red=red4, rol=self.rol, usuario=self.perfil)

        buscarNombre = "test"
        fecha_inicio = "1987-12-28"
        fecha_fin = "3000-12-28"

        url = f"/api/buscarReds/{self.perfil.usuario.pk}/?text={buscarNombre}&fstart={fecha_inicio}&fend={fecha_fin}"

        response =  self.client.get(url, format='json')
        reds = json.loads(response.content)
        
        self.assertEqual(response.status_code , 200)
        self.assertEqual(len(reds), 3)
        self.assertEqual(reds[0]['id'], 1)    
        self.assertEqual(reds[1]['id'], 2) 
        self.assertEqual(reds[2]['id'], 4) 

    def testBuscarRedNameByDates(self):
        fecha = datetime.datetime.now()
        
        proyecto = ProyectoConectate.objects.create(id=3,fecha_inicio=fecha,fecha_fin=fecha)
        #RED.objects.create(id=, proyecto_conectate=proyecto, nombre="", nombre_corto="", descripcion=)
        red1 = RED.objects.create(id=1, id_conectate="1", proyecto_conectate=proyecto, nombre="a", nombre_corto="a", descripcion="a", fecha_inicio=datetime.datetime.strptime('2019-01-02','%Y-%m-%d'),fecha_cierre=datetime.datetime.strptime('2019-12-30','%Y-%m-%d'))
        red2 = RED.objects.create(id=2, id_conectate="2", proyecto_conectate=proyecto, nombre="a", nombre_corto="a", descripcion="a", fecha_inicio=datetime.datetime.strptime('2018-01-01','%Y-%m-%d'),fecha_cierre=datetime.datetime.strptime('2019-06-01','%Y-%m-%d'))
        red3 = RED.objects.create(id=3, id_conectate="3", proyecto_conectate=proyecto, nombre="a", nombre_corto="a", descripcion="a", fecha_inicio=datetime.datetime.strptime('2019-06-01','%Y-%m-%d'),fecha_cierre=datetime.datetime.strptime('2020-01-01','%Y-%m-%d'))
        red4 = RED.objects.create(id=4, id_conectate="4", proyecto_conectate=proyecto, nombre="a", nombre_corto="a", descripcion="a", fecha_inicio=datetime.datetime.strptime('2017-01-01','%Y-%m-%d'),fecha_cierre=datetime.datetime.strptime('2017-12-31','%Y-%m-%d'))

        RolAsignado.objects.create(id_conectate='1', estado=1, red=red1, rol=self.rol, usuario=self.perfil)
        RolAsignado.objects.create(id_conectate='2', estado=1, red=red2, rol=self.rol, usuario=self.perfil)
        RolAsignado.objects.create(id_conectate='3', estado=1, red=red3, rol=self.rol, usuario=self.perfil)
        RolAsignado.objects.create(id_conectate='4', estado=1, red=red4, rol=self.rol, usuario=self.perfil)

        buscarNombre = "b"
        fecha_inicio = "2019-01-01"
        fecha_fin = "2019-12-31"

        url = f"/api/buscarReds/{self.perfil.usuario.pk}/?fstart={fecha_inicio}&fend={fecha_fin}"

        response =  self.client.get(url, format='json')
        reds = json.loads(response.content)
        
        self.assertEqual(response.status_code , 200)
        self.assertEqual(len(reds), 1)    
        self.assertEqual(reds[0]['id'], 1)

    def testBuscarRedNameByOneDate(self):
        fecha = datetime.datetime.now()
        
        proyecto = ProyectoConectate.objects.create(id=3,fecha_inicio=fecha,fecha_fin=fecha)
        #RED.objects.create(id=, proyecto_conectate=proyecto, nombre="", nombre_corto="", descripcion=)
        red1 = RED.objects.create(id=1, id_conectate="1", proyecto_conectate=proyecto, nombre="a", nombre_corto="a", descripcion="a", fecha_inicio=datetime.datetime.strptime('2019-01-02','%Y-%m-%d'),fecha_cierre=datetime.datetime.strptime('2019-12-30','%Y-%m-%d'))
        red2 = RED.objects.create(id=2, id_conectate="2", proyecto_conectate=proyecto, nombre="a", nombre_corto="a", descripcion="a", fecha_inicio=datetime.datetime.strptime('2018-01-01','%Y-%m-%d'),fecha_cierre=datetime.datetime.strptime('2019-06-01','%Y-%m-%d'))
        red3 = RED.objects.create(id=3, id_conectate="3", proyecto_conectate=proyecto, nombre="a", nombre_corto="a", descripcion="a", fecha_inicio=datetime.datetime.strptime('2019-06-01','%Y-%m-%d'),fecha_cierre=datetime.datetime.strptime('2020-01-01','%Y-%m-%d'))
        red4 = RED.objects.create(id=4, id_conectate="4", proyecto_conectate=proyecto, nombre="a", nombre_corto="a", descripcion="a", fecha_inicio=datetime.datetime.strptime('2017-01-01','%Y-%m-%d'),fecha_cierre=datetime.datetime.strptime('2017-12-31','%Y-%m-%d'))

        RolAsignado.objects.create(id_conectate='1', estado=1, red=red1, rol=self.rol, usuario=self.perfil)
        RolAsignado.objects.create(id_conectate='2', estado=1, red=red2, rol=self.rol, usuario=self.perfil)
        RolAsignado.objects.create(id_conectate='3', estado=1, red=red3, rol=self.rol, usuario=self.perfil)
        RolAsignado.objects.create(id_conectate='4', estado=1, red=red4, rol=self.rol, usuario=self.perfil)

        buscarNombre = "b"
        fecha_inicio = "2019-01-01"

        url = f"/api/buscarReds/{self.perfil.usuario.pk}/?fstart={fecha_inicio}"

        response =  self.client.get(url, format='json')
        reds = json.loads(response.content)
        
        self.assertEqual(response.status_code , 200)
        self.assertEqual(len(reds), 2)    
        self.assertEqual(reds[0]['id'], 1)
        self.assertEqual(reds[1]['id'], 3)


class ListarVersionesTestCase(TestCase):

    def setUp(self):
        user = User.objects.create_user(username='test', password='sihdfnssejkhfse', email='test@test.com')
        perfil = Perfil.objects.create(id_conectate='1', usuario=user, estado=1)
        proyecto = ProyectoConectate.objects.create(id_conectate='1', nombre='MISO', codigo='1234', 
            fecha_inicio='2019-03-20', fecha_fin='2019-04-10')
        self.red = RED.objects.create(id_conectate='1', nombre='elRED', descripcion='la descripcion', 
            tipo='video', solicitante='', proyecto_conectate=proyecto)
        Version.objects.create(es_final=False, numero=1, archivos='asd', red=self.red, creado_por=perfil)
        Version.objects.create(es_final=True, numero=2, archivos='asd2', red=self.red, creado_por=perfil)

    def test_respuesta_listar_versiones(self):
        url = '/api/reds/'+str(self.red.pk)+'/versiones/'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, 200)

    def test_contar_versiones(self):
        url = '/api/reds/'+str(self.red.pk)+'/versiones/'
        response = self.client.get(url, format='json')
        data = json.loads(response.content)['context']
        self.assertEqual(len(data), 2)

    def test_listar_versiones(self):
        url = '/api/reds/'+str(self.red.pk)+'/versiones/'
        response = self.client.get(url, format='json')
        data = json.loads(response.content)['context']
        self.assertEqual(data[0]['es_final'], False)
        self.assertEqual(data[1]['es_final'], True)
        self.assertEqual(data[0]['numero'], 1)
        self.assertEqual(data[1]['numero'], 2)
        self.assertEqual(data[0]['archivos'], 'asd')
        self.assertEqual(data[1]['archivos'], 'asd2')

    def test_creadores_versiones(self):
        url = '/api/reds/'+str(self.red.pk)+'/versiones/'
        response = self.client.get(url, format='json')
        data = json.loads(response.content)['context']
        self.assertEqual(data[0]['creado_por']['id_conectate'], '1')
        self.assertEqual(data[1]['creado_por']['id_conectate'], '1')
        self.assertEqual(data[0]['creado_por']['estado'], 1)
        self.assertEqual(data[1]['creado_por']['estado'], 1)
        self.assertEqual(data[0]['creado_por']['usuario']['username'], 'test')
        self.assertEqual(data[1]['creado_por']['usuario']['username'], 'test')

    def test_404_listar_versiones(self):
        url = '/api/reds/'+str(self.red.pk+1)+'/versiones/'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, 404)


class VersionTestCase(TestCase):


    def test_get_info_version(self):
        user = User.objects.create_user(username='test', password='123456', email='test@test.com', first_name='test',
                                        last_name='T')
        perfil = Perfil.objects.create(id_conectate=123, usuario=user, estado=1)
        proyecto = ProyectoConectate.objects.create(id_conectate='1', nombre='MISO', codigo='1234',
                                                    fecha_inicio='2019-03-20', fecha_fin='2019-04-10')
        self.red = RED.objects.create(id_conectate='1', nombre='elRED', descripcion=' ',
                                      tipo='video', solicitante='', proyecto_conectate=proyecto)
        self.version = Version.objects.create(numero=1, red=self.red, creado_por=perfil, fecha_creacion='2019-03-20',
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
        self.version = Version.objects.create(numero=1, red=self.red, creado_por=perfil, fecha_creacion='2019-03-20',
                                              imagen='https://i.pinimg.com/736x/3e/63/03/3e630381b8e25dda523301dc800c8c1d.jpg')
        self.version2 = Version.objects.create(numero=2, red=self.red, creado_por=perfil, fecha_creacion='2019-03-20',
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
        self.version = Version.objects.create(numero=1, red=self.red, creado_por=perfil, fecha_creacion='2019-03-20',
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
        self.version = Version.objects.create(numero=1, red=self.red, creado_por=perfil, fecha_creacion='2019-03-20',
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
        self.version = Version.objects.create(numero=1, red=self.red, creado_por=perfil, fecha_creacion='2019-03-20',
                                              imagen='https://i.pinimg.com/736x/3e/63/03/3e630381b8e25dda523301dc800c8c1d.jpg')

        self.version.recursos.set([recurso1,recurso2])

        url = '/api/versiones/' + str(self.version.pk) + '/recursos/'
        response = self.client.get(url)
        current_data = json.loads(response.content)
        self.assertEqual(current_data['context'][0]['nombre'], 'test')
        self.assertEqual(current_data['context'][1]['nombre'], 'test2')
        self.assertEqual(current_data['context'][0]['tipo'], 'PNG')
        self.assertEqual(current_data['context'][1]['tipo'], 'AVI')

class VersionMarcarTestCase(TestCase):

    def setUp(self):
        user = User.objects.create_user(username='test', password='sihdfnssejkhfse', email='test@test.com')
        perfil = Perfil.objects.create(id_conectate='1', usuario=user, estado=1)
        proyecto = ProyectoConectate.objects.create(id_conectate='1', nombre='MISO', codigo='1234', 
            fecha_inicio='2019-03-20', fecha_fin='2019-04-10')
        self.red = RED.objects.create(id_conectate='1', nombre='elRED', descripcion='la descripcion', 
            tipo='video', solicitante='', proyecto_conectate=proyecto)
        Version.objects.create(es_final=False, numero=1, archivos='asd', red=self.red, creado_por=perfil)
        Version.objects.create(es_final=True, numero=2, archivos='asd2', red=self.red, creado_por=perfil)

    def test_respuesta_listar_versiones(self):
        url = '/api/reds/'+str(self.red.pk)+'/versiones/'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, 200)

    def test_contar_versiones(self):
        url = '/api/reds/'+str(self.red.pk)+'/versiones/'
        response = self.client.get(url, format='json')
        data = json.loads(response.content)['context']
        self.assertEqual(len(data), 2)

    def test_listar_versiones(self):
        url = '/api/reds/'+str(self.red.pk)+'/versiones/'
        response = self.client.get(url, format='json')
        data = json.loads(response.content)['context']
        self.assertEqual(data[0]['es_final'], False)
        self.assertEqual(data[1]['es_final'], True)
        self.assertEqual(data[0]['numero'], 1)
        self.assertEqual(data[1]['numero'], 2)
        self.assertEqual(data[0]['archivos'], 'asd')
        self.assertEqual(data[1]['archivos'], 'asd2')

    def test_creadores_versiones(self):
        url = '/api/reds/'+str(self.red.pk)+'/versiones/'
        response = self.client.get(url, format='json')
        data = json.loads(response.content)['context']
        self.assertEqual(data[0]['creado_por']['id_conectate'], '1')
        self.assertEqual(data[1]['creado_por']['id_conectate'], '1')
        self.assertEqual(data[0]['creado_por']['estado'], 1)
        self.assertEqual(data[1]['creado_por']['estado'], 1)
        self.assertEqual(data[0]['creado_por']['usuario']['username'], 'test')
        self.assertEqual(data[1]['creado_por']['usuario']['username'], 'test')

    def test_404_listar_versiones(self):
        url = '/api/reds/'+str(self.red.pk+1)+'/versiones/'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, 404)
		
    def testMarcarComoVersionFinalJustOne(self):
        url1='/api/versiones/'
        url2='/marcar'
        versionId="1"
        url = url1+versionId+url2

        fecha = datetime.datetime.now()
        proyecto = ProyectoConectate.objects.create(id=1,fecha_inicio=fecha,fecha_fin=fecha)
        red = RED.objects.create(id=1, proyecto_conectate=proyecto)
        versionMain = Version.objects.create(id=1,es_final=False, numero=1, red=red)

        response =  self.client.post(url, format='json')

        versionMainAfter = Version.objects.get(id=1)

        self.assertEqual(response.status_code , 200)
        self.assertEqual(versionMainAfter.es_final,True)

    def testMarcarComoVersionFinalFirstMark(self):
        url1='/api/versiones/'
        url2='/marcar'
        versionId="2"
        url = url1+versionId+url2

        fecha = datetime.datetime.now()
        proyecto = ProyectoConectate.objects.create(id=1,fecha_inicio=fecha,fecha_fin=fecha)
        red = RED.objects.create(id=1, proyecto_conectate=proyecto)
        versionMain = Version.objects.create(id=2,es_final=False, numero=2, red=red)
        versionMain = Version.objects.create(id=1,es_final=False, numero=1, red=red)

        response =  self.client.post(url, format='json')

        versionMainAfter1 = Version.objects.get(id=1)
        versionMainAfter2 = Version.objects.get(id=2)

        self.assertEqual(response.status_code , 200)
        self.assertEqual(versionMainAfter1.es_final,False)
        self.assertEqual(versionMainAfter2.es_final,True)

    def testMarcarComoVersionFinalSecondMark(self):
        url1='/api/versiones/'
        url2='/marcar'
        versionId="2"
        url = url1+versionId+url2

        fecha = datetime.datetime.now()
        proyecto = ProyectoConectate.objects.create(id=1,fecha_inicio=fecha,fecha_fin=fecha)
        red = RED.objects.create(id=1, proyecto_conectate=proyecto)
        versionMain = Version.objects.create(id=2,es_final=False, numero=2, red=red)
        versionMain = Version.objects.create(id=1,es_final=True, numero=1, red=red)

        response =  self.client.post(url, format='json')

        versionMainAfter1 = Version.objects.get(id=1)
        versionMainAfter2 = Version.objects.get(id=2)

        self.assertEqual(response.status_code , 200)
        self.assertEqual(versionMainAfter1.es_final,False)
        self.assertEqual(versionMainAfter2.es_final,True)