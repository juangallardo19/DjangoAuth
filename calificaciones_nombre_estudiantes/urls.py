from django.urls import path
from . import views

urlpatterns = [
    # Auth
    path('login/',    views.vista_login,      name='login'),
    path('logout/',   views.vista_logout,     name='logout'),
    path('usuarios/registrar/', views.registrar_usuario, name='registrar_usuario'),

    # CRUD calificaciones
    path('calificaciones/',              views.listar_calificaciones, name='listar_calificaciones'),
    path('calificaciones/crear/',        views.crear_calificacion,    name='crear_calificacion'),
    path('calificaciones/<int:pk>/editar/',   views.editar_calificacion,   name='editar_calificacion'),
    path('calificaciones/<int:pk>/eliminar/', views.eliminar_calificacion, name='eliminar_calificacion'),

    # Promedio general
    path('promedio-general/', views.promedio_general, name='promedio_general'),
]