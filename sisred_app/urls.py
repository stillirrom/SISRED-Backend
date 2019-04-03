from django.urls import path
from sisred_app.views import views_equipo3

urlpatterns = [

    path('recurso_list/', views.recurso_list, name='recurso_list'),
    path('recurso_get/<int:id>', views.recurso_get, name='recurso_get'),
    path('recurso_put/', views.recurso_put, name='recurso_put'),
    path('recurso_post/', views.recurso_post, name='recurso_post'),
    path('fase_byid', views.fase_byid, name='fase_byid'),


    path('post_proyecto_red/', views_equipo3.post_proyecto_red, name='agregar_proyecto_red'),
    path('detallered/', views_equipo3.get_detallered, name='detallered'),
    path('detallered/metadata/', views_equipo3.get_detallered_metadata, name='detallered'),
    path('detallered/personas/', views_equipo3.get_detallered_personas, name='detallered'),
    path('detallered/recursos/', views_equipo3.get_detallered_recursos, name='detallered'),
    path('detallered/proyectos/', views_equipo3.get_detallered_proyectosred, name='detallered'),
    path('reds/asignados/<int:id>', views_equipo3.get_reds_asignados, name='reds_asignados'),

]
