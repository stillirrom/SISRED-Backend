import csv
import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sisred.settings")
django.setup()
from sisred_app.models import Rol, Perfil, RED, RolAsignado

# Metodo para cargar las asignaciones de los proyectos REDs
with open('C:\\Users\\Usuario\\Desktop\\asignaciones.txt') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            print(f'Nombres de las columnas {", ".join(row)}')
            line_count += 1
        else:
            print(f'\t{row[0]}, {row[1]}, {row[2]}, {row[3]}, {row[4]}, {row[5]}, {row[6]}')
            id_asigancion = row[0]
            id_red = row[1]
            id_usuario = row[3]
            id_rol = row[4]
            estado = row[6]
            rol = Rol.objects.get(id_conectate=id_rol)
            red = RED.objects.get(id_conectate=id_red)
            perfil = Perfil.objects.get(id_conectate=id_usuario)
            rol_asignado = RolAsignado(
                id_conectate=id_asigancion,
                estado=estado,
                red=red,
                rol=rol,
                usuario=perfil,
            )
            rol_asignado.save()
            line_count += 1
    print(f'{line_count} lineas procesadas.')
