from django.urls import path
from . import views

urlpatterns = [
    path('getProyectosRED/', views.getProyectosRED),
    path('getRecurso/', views.getRecurso),
    path('getRED/', views.getRED),
    path('asignaciones/', views.getAsignaciones),
]
