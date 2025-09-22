from django.urls import path
from . import views  # Importa todas las vistas desde views.py

urlpatterns = [
    path('', views.inicio, name='inicio'),  # La URL vacía ('') usará la vista 'inicio'
    path('actividades/', views.actividades, name='actividades'),
    path('reservas/', views.reservas, name='reservas'),
    path('ofertas/', views.ofertas, name='ofertas'),
    path('login/', views.login_view, name='login'),
    path('registro/', views.registro, name='registro'),
    path('logout/', views.logout_view, name='logout'),
    path('perfil/', views.perfil, name='perfil'),
    path('administracion/', views.administracion, name='administracion'),

    # URLs para recuperación de contraseña
    path('password-reset/', views.password_reset_request, name='password_reset_request'),
    path('password-reset/done/', views.password_reset_done, name='password_reset_done'),
    path('password-reset/confirm/<str:token>/', views.password_reset_confirm, name='password_reset_confirm'),
    path('password-reset/complete/', views.password_reset_complete, name='password_reset_complete'),

    # URLs CRUD para Juegos
    path('juegos/', views.lista_juegos, name='lista_juegos'),
    path('juegos/crear/', views.crear_juego, name='crear_juego'),
    path('juegos/editar/<int:id>/', views.editar_juego, name='editar_juego'),
    path('juegos/eliminar/<int:id>/', views.eliminar_juego, name='eliminar_juego'),
    
    # URLs para Carrito
    path('carrito/', views.ver_carrito, name='ver_carrito'),
    path('carrito/agregar/<int:juego_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('carrito/actualizar/<int:item_id>/', views.actualizar_carrito, name='actualizar_carrito'),
    path('carrito/eliminar/<int:item_id>/', views.eliminar_del_carrito, name='eliminar_del_carrito'),
    
    # URLs para Reservas
    path('reservas/lista/', views.lista_reservas, name='lista_reservas'),
    path('reservas/crear/', views.crear_reserva, name='crear_reserva'),
    path('reservas/cancelar/<int:id>/', views.cancelar_reserva, name='cancelar_reserva'),

    
    # CATEGORIAS
    path('terror/', views.terror, name='terror'), 
    path('accion/', views.accion, name='accion'), 
    path('carreras/', views.carreras, name='carreras'), 
    path('mundoabierto/', views.mundoabierto, name='mundoabierto'), 
    path('suspenso/', views.suspenso, name='suspenso'), 

    # JUEGOS
    path('resident_evil/', views.resident_evil, name='resident_evil'), 
    path('outlast/', views.outlast, name='outlast'), 
    path('alien/', views.alien, name='alien'), 
    path('silentHill2/', views.silentHill2, name='silentHill2'), 
    path('horizon/', views.horizon, name='horizon'), 
    path('eldenring/', views.eldenring, name='eldenring'), 
    path('mariokart/', views.mariokart, name='mariokart'), 
    path('projectcars3/', views.projectcars3, name='projectcars3'), 
    path('spiderman/', views.spiderman, name='spiderman'), 
    path('halo3/', views.halo3, name='halo3'), 

    # URLs para Gestión de Juegos (Admin)
    path('admin/juegos/', views.lista_juegos, name='lista_juegos'),
    path('admin/juegos/crear/', views.crear_juego, name='crear_juego'),
    path('admin/juegos/editar/<int:id>/', views.editar_juego, name='editar_juego'),
    path('admin/juegos/eliminar/<int:id>/', views.eliminar_juego, name='eliminar_juego'),
]