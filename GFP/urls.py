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
from upload.views import CFP_app
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', lambda request: redirect('index', permanent=True)),
    path('index/', views.CFP, name='index'),
    path('editar_ajax/', views.editar_image_ajax, name='editar_image_ajax'),
    path('login/', views.Login, name='login'),
    path('perfil/', views.Perfil, name='perfil'),
    path('editar_boleto/<int:id>/', views.editar_boleto, name='editar_boleto'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', views.Register, name='register'),
    path('cfp_app/', views.CFP_app , name='cfp_app'),
    path('ComoFunc/', views.ComoFunciona, name='ComoFunciona')
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
