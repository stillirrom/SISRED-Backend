from django.test import TestCase
from .models import Version, RED, ProyectoConectate, Metadata, Perfil
from django.contrib.auth.models import User
import datetime
import json

# Create your tests here.
class sisred_appTestCase(TestCase):
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
        RED.objects.create(id=1, id_conectate="1", proyecto_conectate=proyecto, nombre="video red", nombre_corto="vred", descripcion="descripcion de video", fecha_inicio=datetime.datetime.now(),fecha_cierre=datetime.datetime.now())
        RED.objects.create(id=2, id_conectate="2", proyecto_conectate=proyecto, nombre="sonido red", nombre_corto="sred", descripcion="descripcion de sonido", fecha_inicio=datetime.datetime.now(),fecha_cierre=datetime.datetime.now())

        buscarNombre = "video"
        fecha_inicio = "1987-12-28"
        fecha_fin = "3000-12-28"

        url = f"/api/buscarReds?text={buscarNombre}&fstart={fecha_inicio}&fend={fecha_fin}"

        response =  self.client.get(url, format='json')
        reds = json.loads(response.content)

        self.assertEqual(response.status_code , 200)
        self.assertEqual(len(reds), 1)    

    def testBuscarRedNameAllByNameNoDates(self):
        fecha = datetime.datetime.now()
        proyecto = ProyectoConectate.objects.create(id=3,fecha_inicio=fecha,fecha_fin=fecha)
        #RED.objects.create(id=, proyecto_conectate=proyecto, nombre="", nombre_corto="", descripcion=)
        RED.objects.create(id=1, id_conectate="1", proyecto_conectate=proyecto, nombre="video red", nombre_corto="vred", descripcion="descripcion de video", fecha_inicio=datetime.datetime.now(),fecha_cierre=datetime.datetime.now())
        RED.objects.create(id=2, id_conectate="2", proyecto_conectate=proyecto, nombre="sonido red", nombre_corto="sred", descripcion="descripcion de sonido", fecha_inicio=datetime.datetime.now(),fecha_cierre=datetime.datetime.now())

        buscarNombre = "video"

        url = f"/api/buscarReds?text={buscarNombre}"

        response =  self.client.get(url, format='json')
        reds = json.loads(response.content)

        self.assertEqual(response.status_code , 200)
        self.assertEqual(len(reds), 1)    

    def testBuscarRedNameByName(self):
        fecha = datetime.datetime.now()
        proyecto = ProyectoConectate.objects.create(id=3,fecha_inicio=fecha,fecha_fin=fecha)
        #RED.objects.create(id=, proyecto_conectate=proyecto, nombre="", nombre_corto="", descripcion=)
        RED.objects.create(id=1, id_conectate="1", proyecto_conectate=proyecto, nombre="video3 red", nombre_corto="vred", descripcion="descripcion de video", fecha_inicio=datetime.datetime.now(),fecha_cierre=datetime.datetime.now())
        RED.objects.create(id=2, id_conectate="2", proyecto_conectate=proyecto, nombre="sonido red", nombre_corto="sred", descripcion="descripcion de sonido", fecha_inicio=datetime.datetime.now(),fecha_cierre=datetime.datetime.now())
        RED.objects.create(id=3, id_conectate="3", proyecto_conectate=proyecto, nombre="video3 red", nombre_corto="sred", descripcion="descripcion de video", fecha_inicio=datetime.datetime.now(),fecha_cierre=datetime.datetime.now())

        buscarNombre = "video3"
        fecha_inicio = "1987-12-28"
        fecha_fin = "3000-12-28"

        url = f"/api/buscarReds?text={buscarNombre}&fstart={fecha_inicio}&fend={fecha_fin}"

        response =  self.client.get(url, format='json')
        reds = json.loads(response.content)
        self.assertEqual(response.status_code , 200)
        self.assertEqual(len(reds), 2)    
        self.assertEqual(reds[0]['id'], 1)    
        self.assertEqual(reds[1]['id'], 3)    

    def testBuscarRedNameByshortName(self):
        fecha = datetime.datetime.now()
        proyecto = ProyectoConectate.objects.create(id=3,fecha_inicio=fecha,fecha_fin=fecha)
        #RED.objects.create(id=, proyecto_conectate=proyecto, nombre="", nombre_corto="", descripcion=)
        RED.objects.create(id=1, id_conectate="1", proyecto_conectate=proyecto, nombre="video3 red", nombre_corto="vred", descripcion="descripcion de video", fecha_inicio=datetime.datetime.now(),fecha_cierre=datetime.datetime.now())
        RED.objects.create(id=2, id_conectate="2", proyecto_conectate=proyecto, nombre="sonido red", nombre_corto="sred", descripcion="descripcion de sonido", fecha_inicio=datetime.datetime.now(),fecha_cierre=datetime.datetime.now())
        RED.objects.create(id=3, id_conectate="3", proyecto_conectate=proyecto, nombre="video3 red", nombre_corto="sred", descripcion="descripcion de video", fecha_inicio=datetime.datetime.now(),fecha_cierre=datetime.datetime.now())

        buscarNombre = "sred"
        fecha_inicio = "1987-12-28"
        fecha_fin = "3000-12-28"

        url = f"/api/buscarReds?text={buscarNombre}&fstart={fecha_inicio}&fend={fecha_fin}"

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
        RED.objects.create(id=1, id_conectate="1", proyecto_conectate=proyecto, nombre="video3 red", nombre_corto="vred", descripcion="descripcion de video", fecha_inicio=datetime.datetime.now(),fecha_cierre=datetime.datetime.now())
        RED.objects.create(id=2, id_conectate="2", proyecto_conectate=proyecto, nombre="sonido red", nombre_corto="sred", descripcion="descripcion de sonido", fecha_inicio=datetime.datetime.now(),fecha_cierre=datetime.datetime.now())
        RED.objects.create(id=3, id_conectate="3", proyecto_conectate=proyecto, nombre="video3 red", nombre_corto="sred", descripcion="descripcion de video", fecha_inicio=datetime.datetime.now(),fecha_cierre=datetime.datetime.now())

        buscarNombre = "descripcion de video"
        fecha_inicio = "1987-12-28"
        fecha_fin = "3000-12-28"

        url = f"/api/buscarReds?text={buscarNombre}&fstart={fecha_inicio}&fend={fecha_fin}"

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
        uno = RED.objects.create(id=1, id_conectate="1", proyecto_conectate=proyecto, nombre="video3 red", nombre_corto="vred", descripcion="descripcion de video", fecha_inicio=datetime.datetime.now(),fecha_cierre=datetime.datetime.now())
        RED.objects.create(id=2, id_conectate="2", proyecto_conectate=proyecto, nombre="sonido red", nombre_corto="sred", descripcion="descripcion de sonido", fecha_inicio=datetime.datetime.now(),fecha_cierre=datetime.datetime.now())
        RED.objects.create(id=3, id_conectate="3", proyecto_conectate=proyecto, nombre="video3 red", nombre_corto="sred", descripcion="descripcion de video", fecha_inicio=datetime.datetime.now(),fecha_cierre=datetime.datetime.now())

        tag = Metadata.objects.create(id = 1,tag="tag1")

        uno.metadata.add(tag)

        buscarNombre = "tag1"
        fecha_inicio = "1987-12-28"
        fecha_fin = "3000-12-28"

        url = f"/api/buscarReds?text={buscarNombre}&fstart={fecha_inicio}&fend={fecha_fin}"

        response =  self.client.get(url, format='json')
        reds = json.loads(response.content)
        
        self.assertEqual(response.status_code , 200)
        self.assertEqual(len(reds), 1)    
        self.assertEqual(reds[0]['id'], 1) 

    def testBuscarRedNameByAllText(self):
        fecha = datetime.datetime.now()
        proyecto = ProyectoConectate.objects.create(id=3,fecha_inicio=fecha,fecha_fin=fecha)

        RED.objects.create(id=1, id_conectate="1", proyecto_conectate=proyecto, nombre="test", nombre_corto="vred", descripcion="descripcion de video", fecha_inicio=datetime.datetime.now(),fecha_cierre=datetime.datetime.now())
        RED.objects.create(id=2, id_conectate="2", proyecto_conectate=proyecto, nombre="sonido red", nombre_corto="test", descripcion="descripcion de sonido", fecha_inicio=datetime.datetime.now(),fecha_cierre=datetime.datetime.now())
        RED.objects.create(id=3, id_conectate="3", proyecto_conectate=proyecto, nombre="video3 red", nombre_corto="sred", descripcion="descripcion de video", fecha_inicio=datetime.datetime.now(),fecha_cierre=datetime.datetime.now())
        RED.objects.create(id=4, id_conectate="4", proyecto_conectate=proyecto, nombre="video3 red", nombre_corto="sred", descripcion="descripcion test de video", fecha_inicio=datetime.datetime.now(),fecha_cierre=datetime.datetime.now())

        buscarNombre = "test"
        fecha_inicio = "1987-12-28"
        fecha_fin = "3000-12-28"

        url = f"/api/buscarReds?text={buscarNombre}&fstart={fecha_inicio}&fend={fecha_fin}"

        response =  self.client.get(url, format='json')
        reds = json.loads(response.content)
        
        self.assertEqual(response.status_code , 200)
        self.assertEqual(len(reds), 3)
        self.assertEqual(reds[0]['id'], 2)    
        self.assertEqual(reds[1]['id'], 4) 
        self.assertEqual(reds[2]['id'], 1) 

    def testBuscarRedNameByDates(self):
        fecha = datetime.datetime.now()
        
        proyecto = ProyectoConectate.objects.create(id=3,fecha_inicio=fecha,fecha_fin=fecha)
        #RED.objects.create(id=, proyecto_conectate=proyecto, nombre="", nombre_corto="", descripcion=)
        RED.objects.create(id=1, id_conectate="1", proyecto_conectate=proyecto, nombre="a", nombre_corto="a", descripcion="a", fecha_inicio=datetime.datetime.strptime('2019-01-02','%Y-%m-%d'),fecha_cierre=datetime.datetime.strptime('2019-12-30','%Y-%m-%d'))
        RED.objects.create(id=2, id_conectate="2", proyecto_conectate=proyecto, nombre="a", nombre_corto="a", descripcion="a", fecha_inicio=datetime.datetime.strptime('2018-01-01','%Y-%m-%d'),fecha_cierre=datetime.datetime.strptime('2019-06-01','%Y-%m-%d'))
        RED.objects.create(id=3, id_conectate="3", proyecto_conectate=proyecto, nombre="a", nombre_corto="a", descripcion="a", fecha_inicio=datetime.datetime.strptime('2019-06-01','%Y-%m-%d'),fecha_cierre=datetime.datetime.strptime('2020-01-01','%Y-%m-%d'))
        RED.objects.create(id=4, id_conectate="4", proyecto_conectate=proyecto, nombre="a", nombre_corto="a", descripcion="a", fecha_inicio=datetime.datetime.strptime('2017-01-01','%Y-%m-%d'),fecha_cierre=datetime.datetime.strptime('2017-12-31','%Y-%m-%d'))

        buscarNombre = "b"
        fecha_inicio = "2019-01-01"
        fecha_fin = "2019-12-31"

        url = f"/api/buscarReds?fstart={fecha_inicio}&fend={fecha_fin}"

        response =  self.client.get(url, format='json')
        reds = json.loads(response.content)
        
        self.assertEqual(response.status_code , 200)
        self.assertEqual(len(reds), 1)    
        self.assertEqual(reds[0]['id'], 1)

    def testBuscarRedNameByOneDate(self):
        fecha = datetime.datetime.now()
        
        proyecto = ProyectoConectate.objects.create(id=3,fecha_inicio=fecha,fecha_fin=fecha)
        #RED.objects.create(id=, proyecto_conectate=proyecto, nombre="", nombre_corto="", descripcion=)
        RED.objects.create(id=1, id_conectate="1", proyecto_conectate=proyecto, nombre="a", nombre_corto="a", descripcion="a", fecha_inicio=datetime.datetime.strptime('2019-01-02','%Y-%m-%d'),fecha_cierre=datetime.datetime.strptime('2019-12-30','%Y-%m-%d'))
        RED.objects.create(id=2, id_conectate="2", proyecto_conectate=proyecto, nombre="a", nombre_corto="a", descripcion="a", fecha_inicio=datetime.datetime.strptime('2018-01-01','%Y-%m-%d'),fecha_cierre=datetime.datetime.strptime('2019-06-01','%Y-%m-%d'))
        RED.objects.create(id=3, id_conectate="3", proyecto_conectate=proyecto, nombre="a", nombre_corto="a", descripcion="a", fecha_inicio=datetime.datetime.strptime('2019-06-01','%Y-%m-%d'),fecha_cierre=datetime.datetime.strptime('2020-01-01','%Y-%m-%d'))
        RED.objects.create(id=4, id_conectate="4", proyecto_conectate=proyecto, nombre="a", nombre_corto="a", descripcion="a", fecha_inicio=datetime.datetime.strptime('2017-01-01','%Y-%m-%d'),fecha_cierre=datetime.datetime.strptime('2017-12-31','%Y-%m-%d'))

        buscarNombre = "b"
        fecha_inicio = "2019-01-01"

        url = f"/api/buscarReds?fstart={fecha_inicio}"

        response =  self.client.get(url, format='json')
        reds = json.loads(response.content)
        
        self.assertEqual(response.status_code , 200)
        self.assertEqual(len(reds), 2)    
        self.assertEqual(reds[0]['id'], 1)
        self.assertEqual(reds[1]['id'], 3)


class ListarVersionesTestCase(TestCase):

    red = None

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
