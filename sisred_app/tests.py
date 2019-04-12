from django.test import TestCase
from .models import Version, RED, ProyectoConectate, Perfil
from django.contrib.auth.models import User
import json
import datetime

# Create your tests here.
class sisred_appTestCase(TestCase):

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
