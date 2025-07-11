from django import forms
from .models import Imagem, UserProfile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm

# Lista de tipos de conta disponíveis para seleção no formulário
TIPOS = [
    ('CPFL','CPFL'),
    ('Naturgy','Naturgy'),
    ('Energisa','Energisa'),
    ('Vivo','Vivo'),
]

# Formulário que permite ao usuário enviar uma imagem do boleto
# e selecionar o tipo de conta correspondente para processamento
class ContaEImagemForm(forms.ModelForm):
    tipo_conta = forms.ChoiceField(
    choices=TIPOS,
    widget=forms.Select,
    required=True
    )

    class Meta:
        model = Imagem
        fields = ['imagem','tipo_conta']


# Formulário personalizado para registro de novos usuários
# Herda de UserCreationForm e adiciona campos para username, email, senha e confirmação de senha
# Define widgets customizados para melhorar a experiência do usuário com placeholders e classes CSS
class CadastroForm(UserCreationForm):
    username = forms.CharField(max_length=150,required=True,widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Digite seu Nome'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder':'Digite seu Email'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder':'Digite sua Senha'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder':'Confirme sua Senha'}))
    
    class Meta:
        model = User
        fields = ["username","email", "password1", "password2"]



# Formulário personalizado para login de usuários
# Estende AuthenticationForm do Django e personaliza os campos de username e senha
# Adiciona atributos CSS e placeholders para melhorar a usabilidade e aparência do formulário
class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(max_length=150,required=True,widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Digite seu Nome'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder':'Digite sua Senha'}))


# Formulário para edição dos dados dos boletos já enviados
# Baseado no model Imagem, permite editar a imagem, tipo da conta, data e valor do boleto
class ImagemForm(forms.ModelForm):
    class Meta:
        model = Imagem
        fields = ['imagem','tipo_conta','boleto_data','boleto_valor']


# Formulário para envio/edição da imagem de perfil do usuário
# Baseado no model UserProfile, permite enviar ou alterar a foto de perfil
# O campo 'profile_pics' utiliza um widget customizado para o input de arquivo, com id 'fileInput'
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_pics']
        widgets = {
            'profile_pics': forms.ClearableFileInput(attrs={
                'id': 'fileInput'
            })
        }
