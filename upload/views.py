from django.shortcuts import render, redirect,get_object_or_404
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from .models import Imagem, tipo_conta, UserProfile
from .forms import ContaEImagemForm, ImagemForm, UserProfileForm
from .OCR import OCR
from decimal import Decimal
from datetime import datetime
from .forms import CadastroForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .forms import CustomLoginForm
from django.contrib import messages
import os


def index(request):
    return render(request, 'index.html')


@login_required
def editar_boleto(request, id):
    print("POST Data:", request.POST) 

    try:
        imagem = Imagem.objects.get(id=id)
    
    except Imagem.DoesNotExist:
        return HttpResponse("Boleto não encontrado", status=404)

    if request.method == 'POST':
        tipo_conta = request.POST.get('tipo_conta')
        data = request.POST.get('boleto_data')
        valor = request.POST.get('boleto_valor')
        action_type = request.POST.get('action_type')

        if action_type == 'delete':
            imagem.delete()
            return redirect('perfil')

        try:
            data = datetime.strptime(data, '%Y-%m-%d').date()
        except ValueError:
            return HttpResponse("Data inválida", status=400)
        
        try:
            valor = Decimal(valor)
        except(ValueError, Decimal.InvalidOperatiom):
            return HttpResponse("Valor inválido", status=400)

        imagem.tipo_conta = tipo_conta
        imagem.boleto_data = data
        imagem.boleto_valor = valor
        imagem.save()

        return redirect('perfil')
    else:
        return render(request, "perfil.html", {'imagem':imagem})


@login_required
def extrair_dados(request):
    #boleto_texto = None
    ocr_data = None
    ocr_valor = None
    ocr_valor_final = None

    if request.method == 'POST':
       form = ContaEImagemForm(request.POST, request.FILES)
       tipo_conta = request.POST.get('tipo_conta')
       
       if form.is_valid():
            imagem = form.save(commit=False)
            imagem.user = request.user
            imagem.save()
            
            caminho_imagem = imagem.imagem.path

            ocr = OCR(caminho_imagem,tipo_conta)
            ocr_data, ocr_valor = ocr.pegar_coordenadas()
            
            if ocr_data == "" or ocr_valor == "":
                if imagem.imagem:
                    imagem.imagem.delete(save=False)
                imagem.delete()
                messages.error(request, "Não conseguimos extrair os dados do boleto. Tente novamente com uma imagem de melhor qualidade.")
                return redirect('extrair_dados')
            
            ocr_valor_final = Decimal(ocr_valor.replace("R$","").strip().replace(",", "."))
            imagem.boleto_data = datetime.strptime(ocr_data, "%d/%m/%Y").date()
            imagem.boleto_valor = ocr_valor_final
            imagem.save()

            #if os.path.isfile(caminho_imagem):
             #   os.remove(caminho_imagem)
              #  imagem.imagem = None
               # imagem.save()

    else:
        form = ContaEImagemForm()
    
    dados_extraidos = Imagem.objects.filter(user=request.user).values('boleto_data', 'boleto_valor', 'tipo_conta')
    return render(request, 'extrair_dados.html', {
        'form':form,
        'ocr_data': ocr_data,
        'ocr_valor_final': ocr_valor_final,
        'dados_extraidos': list(dados_extraidos)
        })


def como_funciona(request):
    return render(request, 'como_funciona.html')


def login_view(request):
    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user) # funcao do django
            return redirect('index')
    else:
        form = CustomLoginForm()

    return render(request, 'login.html', {'form': form})


def register_view(request):
    if request.method == 'POST':
        form = CadastroForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login_view')
    else:
        form = CadastroForm()
    return render(request, 'register.html', {'form': form})


@login_required
def perfil(request):
    usuario = request.user
    imagens = Imagem.objects.filter(user=request.user)
    
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    form = UserProfileForm(instance=profile)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user.userprofile)        
        if form.is_valid():
            form.save()
            return redirect('perfil')
    else:
        form = UserProfileForm(instance=request.user.userprofile)
 
    return render(request, 'perfil.html', {
        'usuario': usuario,
        'imagens': imagens,
        'tipo_conta': tipo_conta,
        'form': form,
    })


@login_required
def editar_boleto_ajax(request, imagem_id):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        #imagem_id = request.POST.get('image_id')
        imagem = get_object_or_404(Imagem, id=imagem_id,user=request.user)
        form = ImagemForm(request.POST,request.FILES, instance=imagem)
        if form.is_valid():
            form.save()
            return JsonResponse({'status':'success'})
        else:
            return JsonResponse({'status':'error', 'errors': form.errors})
    return JsonResponse({'status':'invalid'})   


@login_required
def apagar_imagem(request, imagem_id):
    imagem = get_object_or_404(Imagem, id=imagem_id, user=request.user)
    if request.method == 'POST':
        imagem.delete()
        return redirect('perfil')
    return render(request, 'confirmar_delete.html', {'imagem': imagem})






