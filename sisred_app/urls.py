from django.urls import path
from sisred_app import views

urlpatterns = [
    path('proyectosred/', views.getProyectosRED),
    path('recursos/', views.getRecurso),
    path('reds/', views.getRED),
    path('roles/', views.getRoles),
    path('estados/', views.getEstados),
    path('fases/', views.getFases),
    path('proyectosconectate/<int:id>', views.getProyectoContectatePorId),
    path('proyectosconectate/<int:id>/reds', views.getRedDeProyectoContectatePorId),
    path('subirred/', views.subirRed),
]
