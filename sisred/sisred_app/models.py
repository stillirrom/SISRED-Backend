from django.db import models
import datetime

# Create your models here.

class Notificacion(models.Model):
    mensaje = models.TextField()
    fecha = models.DateField(default=datetime.date.today)

    def __str__(self):
        return 'Notificacion: ' + self.name


class Estado(models.Model):
    nombre_estado = models.CharField(max_length=50)

    def __str__(self):
        return 'Estado: ' + self.name


class HistorialEstados(models.Model):
    fecha_cambio = models.DateField(default=datetime.date.today)
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE)

    def __str__(self):
        return 'HistorialEstados: ' + self.name



class Metadata(models.Model):
    tag = models.CharField(max_length=50)

    def __str__(self):
        return "Metadata: "+self.tag


class Recurso(models.Model):
    nombre = models.CharField(max_length=50)
    archivo = models.CharField(max_length=200)
    fecha_creacion = models.DateField(default=datetime.date.today)
    fecha_ultima_modificacion = models.DateField(default=datetime.date.today)
    tipo = models.CharField(max_length=50)
    descripcion = models.TextField()
    metadata = models.ManyToManyField(Metadata)

    def __str__(self):
        return "Recurso: "+self.nombre



class ProyectoConectate(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return 'Proyecto conectate: ' + self.nombre


class RED(models.Model):
    codigo = models.CharField(max_length=50)
    nombre = models.CharField(max_length=100)
    nombre_corto = models.CharField(max_length=50)
    descripcion = models.TextField()
    fecha_inicio = models.DateField()
    fecha_cierre = models.DateField()
    fecha_creacion = models.DateField(default=datetime.date.today)
    porcentaje_avance = models.IntegerField()
    tipo = models.CharField(max_length=50)
    solicitante = models.CharField(max_length=50)
    proyecto_conectate = models.ForeignKey(ProyectoConectate, on_delete=models.CASCADE)
    recursos = models.ManyToManyField(Recurso)
    metadata = models.ManyToManyField(Metadata)

    def __str__(self):
        return 'Red: ' + self.codigo


class ProyectoRED(models.Model):
    nombre = models.CharField(max_length=50)
    tipo = models.CharField(max_length=50)
    red = models.ForeignKey(RED, on_delete=models.CASCADE)

    def __str__(self):
        return "Proyecto RED: "+self.nombre


class Version(models.Model):
    es_final = models.BooleanField(default=False)
    numero = models.IntegerField()
    red = models.ForeignKey(RED, on_delete=models.CASCADE)

    def __str__(self):
        return 'Version: ' + self.name


class Comentario(models.Model):
    contenido = models.TextField()
    #usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    version = models.ForeignKey(Version, on_delete=models.CASCADE)

    def __str__(self):
        return 'Comentario: ' + self.name