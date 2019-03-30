from django.urls import path, include
from . import views


app_name = 'sisred_app'

urlpatterns = [
    path('users/', views.getAllUser, name='allUsers'),
    path('users/<int:id>/', views.getUser, name='getUserId'),
    path('users/add/', views.postUser, name='addUser'),
    path('users/update/<int:id>/', views.putUser, name='updateUser'),
    path('users/delete/<int:id>/', views.deleteUser, name='deleteUser'),
    path('reds/relacionados/<int:id>', views.get_reds_relacionados, name='reds_relacionados'),
    path('getRecurso/<int:id>/', views.getRecurso, name='getRecurso'),
    path('getRedDet/<int:id>/', views.getRedDet, name='getRedDet'),
    path('getUserAut/', views.getUserAut, name='getUserAut'),
    path('update_sisred/', views.update_sisred, name='update_sisred'),
    path('reds/', views.get_red, name='reds'),
    path('sisred_create/', views.sisred_create, name='sisred_create'),
    path('sisred_remove/', views.sisred_remove, name='sisred_remove'),
    path('asignaciones/', views.getAllAsignaciones, name='getAllAsignaciones'),
    path('asignaciones/add/', views.postRolAsignado, name='addRolAsignado')
]