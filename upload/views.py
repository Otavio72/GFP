from django.shortcuts import render, redirect,get_object_or_404
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from .models import Image, TIPOS, UserProfile
from .forms import ContaEImagemForm, ImageForm, UserProfileForm
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


def CFP(request):
    return render(request, 'index.html')


@login_required
def editar_boleto(request, id):
    print("POST Data:", request.POST) 

    try:
        image = Image.objects.get(id=id)
    
    except Image.DoesNotExist:
        return HttpResponse("Boleto não encontrado", status=404)

    if request.method == 'POST':
        escolha = request.POST.get('escolha')
        data = request.POST.get('boleto_data')
        valor = request.POST.get('boleto_valor')
        action_type = request.POST.get('action_type')

        if action_type == 'delete':
            image.delete()
            return redirect('perfil')

        try:
            data = datetime.strptime(data, '%Y-%m-%d').date()
        except ValueError:
            return HttpResponse("Data inválida", status=400)
        
        try:
            valor = Decimal(valor)
        except(ValueError, Decimal.InvalidOperatiom):
            return HttpResponse("Valor inválido", status=400)

        image.escolha = escolha
        image.boleto_data = data
        image.boleto_valor = valor
        image.save()

        return redirect('perfil')
    else:
        return render(request, "perfil.html", {'image':image})


@login_required
def CFP_app(request):
    boleto_texto = None
    ocr_data = None
    ocr_valor = None
    ocr_valorf = None

    if request.method == 'POST':
       form = ContaEImagemForm(request.POST, request.FILES)
       tipo = request.POST.get('escolha')
       
       if form.is_valid():
            imagem = form.save(commit=False)
            imagem.user = request.user
            imagem.save()
            
            caminho_imagem = imagem.image.path

            ocr = OCR(caminho_imagem,tipo)
            ocr_data, ocr_valor = ocr.pegar_coordenadas()
            
            if ocr_data == "" or ocr_valor == "":
                if imagem.image:
                    imagem.image.delete(save=False)
                imagem.delete()
                messages.error(request, "Não conseguimos extrair os dados do boleto. Tente novamente com uma imagem de melhor qualidade.")
                return redirect('cfp_app')
            
            ocr_valorf = Decimal(ocr_valor.replace("R$","").strip().replace(",", "."))
            imagem.boleto_data = datetime.strptime(ocr_data, "%d/%m/%Y").date()
            imagem.boleto_valor = ocr_valorf
            imagem.save()

            if os.path.isfile(caminho_imagem):
                os.remove(caminho_imagem)
                imagem.image = None
                imagem.save()

    else:
        form = ContaEImagemForm()
    
    dados = Image.objects.filter(user=request.user).values('boleto_data', 'boleto_valor', 'escolha')
    return render(request, 'cfp_app.html', {
        'form':form,
        'ocr_data': ocr_data,
        'ocr_valorf': ocr_valorf,
        'dados': list(dados)
        })


def ComoFunciona(request):
    return render(request, 'ComoFunc.html')


def Login(request):
    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
    else:
        form = CustomLoginForm()

    return render(request, 'login.html', {'form': form})


def Register(request):
    if request.method == 'POST':
        form = CadastroForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CadastroForm()
    return render(request, 'register.html', {'form': form})


@login_required
def Perfil(request):
    usuario = request.user
    imagens = Image.objects.filter(user=request.user)
    
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
        'TIPOS': TIPOS,
        'form': form,
    })


@login_required
def editar_image_ajax(request, image_id):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        image_id = request.POST.get('image_id')
        image = get_object_or_404(Image, id=image_id,user=request.user)
        form = ImageForm(request.POST,request.FILES, instance=image)
        if form.is_valid():
            form.save()
            return JsonResponse({'status':'success'})
        else:
            return JsonResponse({'status':'error', 'errors': form.errors})
    return JsonResponse({'status':'invalid'})   


@login_required
def apagar_image(request, image_id):
    image = get_object_or_404(Image, id=image_id, user=request.user)
    if request.method == 'POST':
        image.delete()
        return redirect('perfil')
    return render(request, 'confirmar_delete.html', {'image': image})






