from django.db import models
from django.contrib.auth.models import User
# Create your models here.

# Lista de tipos de boleto recebidos e usados para seleção no formulário
tipo_conta = [
    ('CPFL', 'CPFL'),
    ('Naturgy', 'Naturgy'),
    ('Energisa', 'Energisa'),
    ('Vivo', 'Vivo'),
]

# Model que armazena os dados extraidos e selecionados referentes aos boletos enviados
class Imagem(models.Model):
    imagem = models.ImageField(upload_to='boletos/')
    description = models.TextField(null=True, blank=True)
    tipo_conta = models.CharField(max_length=50, choices=tipo_conta, default='CPFL')
    boleto_data = models.DateField(max_length=10, null=True, blank=True)
    boleto_valor = models.DecimalField(decimal_places=2,max_digits=6, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.description
    
    class Meta:
        ordering = ['boleto_data']

# Model que adiciona campos adicionais no User
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pics = models.ImageField(upload_to='profile_pics/', default='profile_pics/default.jpg')

    def __str__(self):
        return f'{self.user.username} Profile'
    