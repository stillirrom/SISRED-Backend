from django.urls import path
from . import views

urlpatterns = [

    path('post_proyecto_red/', views.post_proyecto_red, name='agregar_proyecto_red'),

]
