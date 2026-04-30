from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.db.models import Avg
from django.contrib import messages
from .models import Calificacion
from .forms import LoginForm, RegistroUsuarioForm, CalificacionForm


def es_admin(user):
    return user.is_superuser or user.is_staff

def es_docente(user):
    return user.groups.filter(name='Docentes').exists() or es_admin(user)


def vista_login(request):
    if request.user.is_authenticated:
        return redirect('listar_calificaciones')

    form = LoginForm(data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.get_user()
        login(request, user)
        messages.success(request, f'Bienvenido, {user.get_full_name() or user.username}')
        return redirect('listar_calificaciones')

    return render(request, 'calificaciones/login.html', {'form': form})


def vista_logout(request):
    logout(request)
    messages.info(request, 'Sesión cerrada correctamente.')
    return redirect('login')


def registrar_usuario(request):
    if request.user.is_authenticated and not es_admin(request.user):
        return redirect('listar_calificaciones')

    form = RegistroUsuarioForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        usuario = form.save()
        messages.success(request, f'Usuario {usuario.username} creado. Ahora puedes iniciar sesión.')
        return redirect('login')
    return render(request, 'calificaciones/registro_usuario.html', {'form': form})

@login_required
def listar_calificaciones(request):
    calificaciones   = Calificacion.objects.all().order_by('nombre_estudiante')
    promedio_general = Calificacion.objects.aggregate(
        Avg('promedio')
    )['promedio__avg']

    return render(request, 'calificaciones/listar.html', {
        'calificaciones':   calificaciones,
        'promedio_general': promedio_general,
        'es_admin':         es_admin(request.user),
    })


@login_required
def crear_calificacion(request):
    form = CalificacionForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Calificación registrada correctamente.')
        return redirect('listar_calificaciones')
    return render(request, 'calificaciones/crear.html', {'form': form})


@login_required
def editar_calificacion(request, pk):
    calificacion = get_object_or_404(Calificacion, pk=pk)
    form = CalificacionForm(request.POST or None, instance=calificacion)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Calificación actualizada.')
        return redirect('listar_calificaciones')
    return render(request, 'calificaciones/editar.html', {
        'form': form, 'calificacion': calificacion
    })


@login_required
@user_passes_test(es_admin)
def eliminar_calificacion(request, pk):
    calificacion = get_object_or_404(Calificacion, pk=pk)
    if request.method == 'POST':
        calificacion.delete()
        messages.success(request, 'Registro eliminado.')
        return redirect('listar_calificaciones')
    return render(request, 'calificaciones/eliminar.html', {
        'calificacion': calificacion
    })


@login_required
def promedio_general(request):
    promedio = Calificacion.objects.aggregate(
        Avg('promedio')
    )['promedio__avg']
    total = Calificacion.objects.count()
    return render(request, 'calificaciones/promedio_general.html', {
        'promedio': promedio,
        'total':    total,
    })