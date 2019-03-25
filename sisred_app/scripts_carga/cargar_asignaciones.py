import csv
import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sisred.settings")
django.setup()

from sisred_app.models import Rol, Perfil, RED, RolAsignado
from django.contrib.auth.models import User
from datetime import datetime

#Metodo para cargar las asignaciones de los proyectos REDs
with open('C:\\Users\\Usuario\\Desktop\\asignaciones.txt') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            print(f'Nombres de las columnas {", ".join(row)}')
            line_count += 1
        else:
            print(f'\t{row[2]}, {row[4]}, {row[5]}, {row[12]}')
            id_red = row[2]
            id_usuario = row[4]
            id_rol = row[5]
            fecha_inicio_temp = row[12]
            rol = Rol.objects.get(nombre=id_rol)
            usuario = User.objects.get(username=id_usuario)
            red = RED.objects.get(codigo=id_red)
            perfil = Perfil.objects.get(usuario=usuario)
            fecha = datetime.strftime(fecha_inicio_temp, '%d/$m/$Y')
            rol_asignado = RolAsignado(
                fecha_inicio=fecha,
                red=red,
                rol=rol,
                usuario=perfil
            )
            rol_asignado.save()
            line_count += 1
    print(f'{line_count} lineas procesadas.')
