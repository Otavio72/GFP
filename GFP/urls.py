"""
URL configuration for GFP project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.shortcuts import redirect
from django.contrib import admin
from django.conf import settings
from django.urls import path
from django.conf.urls.static import static
from upload import views
from django.contrib.auth.views import LogoutView

# Rotas para as paginas do site
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', lambda request: redirect('index', permanent=True)),
    path('index/', views.index, name='index'),
    path('editar_boleto_ajax/', views.editar_boleto_ajax, name='editar_boleto_ajax'), # Inicia o AJAX do editar boleto
    path('login_view/', views.login_view, name='login_view'),
    path('perfil/', views.perfil, name='perfil'),
    path('editar_boleto/<int:id>/', views.editar_boleto, name='editar_boleto'),
    path('logout/', LogoutView.as_view(next_page='login_view'), name='logout'),
    path('register_view/', views.register_view, name='register_view'),
    path('extrair_dados/', views.extrair_dados , name='extrair_dados'),
    path('como_funciona/', views.como_funciona, name='como_funciona')
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
