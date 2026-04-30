from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from .models import Calificacion

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Usuario'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Contraseña'
        })
    )

class RegistroUsuarioForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name',
                  'password1', 'password2']

class CalificacionForm(forms.ModelForm):
    class Meta:
        model  = Calificacion
        exclude = ['promedio']   # promedio se calcula automáticamente
        widgets = {
            'nombre_estudiante': forms.TextInput(attrs={'class':'form-control'}),
            'identificacion':    forms.TextInput(attrs={'class':'form-control'}),
            'asignatura':        forms.TextInput(attrs={'class':'form-control'}),
            'nota1': forms.NumberInput(attrs={'class':'form-control','step':'0.01'}),
            'nota2': forms.NumberInput(attrs={'class':'form-control','step':'0.01'}),
            'nota3': forms.NumberInput(attrs={'class':'form-control','step':'0.01'}),
        }