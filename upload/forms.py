from django import forms
from .models import Imagem, UserProfile
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
    tipo_conta = forms.ChoiceField(
    choices=TIPOS,
    widget=forms.Select,
    required=True
    )

    class Meta:
        model = Imagem
        fields = ['imagem','tipo_conta']


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


class ImagemForm(forms.ModelForm):
    class Meta:
        model = Imagem
        fields = ['imagem','tipo_conta','boleto_data','boleto_valor']


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_pics']
        widgets = {
            'profile_pics': forms.ClearableFileInput(attrs={
                'id': 'fileInput'
            })
        }
