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


@login_required
@user_passes_test(es_admin)
def registrar_usuario(request):
    form = RegistroUsuarioForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        usuario = form.save()
        messages.success(request, f'Usuario {usuario.username} creado.')
        return redirect('listar_calificaciones')
    return render(request, 'calificaciones/registro_usuario.html', {'form': form})