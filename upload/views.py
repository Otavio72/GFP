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


# Renderiza a página inicial do sistema (index.html)
def index(request):
    return render(request, 'index.html')


# View para editar ou excluir um boleto.
# - Recupera o boleto pelo ID.
# - Se o método for POST:
#     - Se a ação for 'delete', exclui o boleto e redireciona para o perfil.
#     - Caso contrário, atualiza os campos com os novos dados enviados.
# - Se for GET, renderiza a página de perfil com os dados do boleto.
@login_required
def editar_boleto(request, id):
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



# Processa o envio de um boleto e extrai seus dados via OCR:
# - Se o método for POST:
#     - Recebe o formulário com o tipo de conta e o arquivo enviado.
#     - Salva a imagem na pasta /media/boletos.
#     - Passa o caminho da imagem e o tipo da conta para o OCR.
#     - Se os dados forem extraídos com sucesso:
#         - Converte o valor e a data para os formatos corretos.
#         - Salva as informações no banco de dados.
#     - Caso contrário, exibe uma mensagem de erro e exclui a imagem.
# - Se for GET, exibe o formulário vazio.
# Por fim, renderiza a página 'extrair_dados.html' com os dados extraídos do usuário.
@login_required
def extrair_dados(request):
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

    else:
        form = ContaEImagemForm()
    
    dados_extraidos = Imagem.objects.filter(user=request.user).values('boleto_data', 'boleto_valor', 'tipo_conta')
    return render(request, 'extrair_dados.html', {
        'form':form,
        'ocr_data': ocr_data,
        'ocr_valor_final': ocr_valor_final,
        'dados_extraidos': list(dados_extraidos)
        })


# Renderiza a página Como_Funciona (como_funciona.html)
def como_funciona(request):
    return render(request, 'como_funciona.html')


# View para autenticação de usuários:
# - Se método for POST:
#     - Instancia CustomLoginForm com os dados enviados.
#     - Se válido, faz login (via django) e redireciona para index.
# - Se método for GET:
#     - Cria um formulário em branco (CustomLoginForm).
# Exibe sempre a template 'login.html' com o formulário.
def login_view(request):
    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
    else:
        form = CustomLoginForm()

    return render(request, 'login.html', {'form': form})


# View responsável pelo registro de novos usuários:
# - Se o método for POST:
#     - Instancia o CadastroForm com os dados recebidos e valida o formulário.
#     - Se for válido, salva o novo usuário no banco de dados e redireciona para a página de login.
# - Se o método for GET:
#     - Instancia um CadastroForm vazio.
# Sempre renderiza a página de registro (register.html) com o formulário.
def register_view(request):
    if request.method == 'POST':
        form = CadastroForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login_view')
    else:
        form = CadastroForm()
    return render(request, 'register.html', {'form': form})



# View da página de perfil do usuário.
# - Recupera o usuário logado e as imagens enviadas por ele.
# - Garante que o perfil do usuário existe usando get_or_create().
# - Se o método for POST:
#     - Instancia o formulário UserProfileForm com os dados recebidos.
#     - Se o formulário for válido, salva as alterações no banco de dados e redireciona para a mesma página.
# - Se o método for GET:
#     - Instancia o formulário com os dados atuais do perfil do usuário.
# Sempre renderiza a página perfil.html com os dados do usuário, suas imagens e o formulário.
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



# View para editar um boleto via AJAX (requisição assíncrona).
# - Verifica se a requisição é do tipo POST e feita via XMLHttpRequest (AJAX).
# - Busca a imagem correspondente ao ID informado e pertencente ao usuário logado.
# - Instancia o formulário ImagemForm com os dados recebidos.
# - Se o formulário for válido, salva as alterações e retorna uma resposta JSON de sucesso.
# - Caso contrário, retorna os erros do formulário em formato JSON.
# - Se a requisição for inválida, retorna status 'invalid'.
@login_required
def editar_boleto_ajax(request, imagem_id):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        imagem = get_object_or_404(Imagem, id=imagem_id,user=request.user)
        form = ImagemForm(request.POST,request.FILES, instance=imagem)
        if form.is_valid():
            form.save()
            return JsonResponse({'status':'success'})
        else:
            return JsonResponse({'status':'error', 'errors': form.errors})
    return JsonResponse({'status':'invalid'})   



# Apaga a imagem do banco de dados
# - Verifica se a imagem existe e pertence ao usuário logado
# - Se for método POST, deleta a imagem
# - Redireciona para a página de perfil
@login_required
def apagar_imagem(request, imagem_id):
    imagem = get_object_or_404(Imagem, id=imagem_id, user=request.user)
    if request.method == 'POST':
        imagem.delete()
    
    return redirect('perfil')
    
