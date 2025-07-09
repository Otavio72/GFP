from django import forms
from .models import Image, UserProfile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm

TIPOS = [
    ('CPFL','CPFL'),
    ('Naturgy','Naturgy'),
    ('Energisa','Energisa'),
    ('Vivo','Vivo'),
]


class ContaEImagemForm(forms.ModelForm):
    escolha = forms.ChoiceField(
    choices=TIPOS,
    widget=forms.Select,
    required=True
    )

    class Meta:
        model = Image
        fields = ['image','escolha']


class CadastroForm(UserCreationForm):
    username = forms.CharField(max_length=150,required=True,widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Digite seu Nome'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder':'Digite seu Email'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder':'Digite sua Senha'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder':'Confirme sua Senha'}))
    
    class Meta:
        model = User
        fields = ["username","email", "password1", "password2"]


class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(max_length=150,required=True,widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Digite seu Nome'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder':'Digite sua Senha'}))


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['image','escolha','boleto_data','boleto_valor']


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_pics']
        widgets = {
            'profile_pics': forms.ClearableFileInput(attrs={
                'id': 'fileInput'
            })
        }
