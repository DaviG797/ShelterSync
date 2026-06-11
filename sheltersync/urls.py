"""
URL configuration for sheltersync project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.contrib import admin
from django.contrib.auth import views as auth_views
from vagas.views import (
    AcolhidoListView,
    AcolhidoCreateView,
    AcolhidoUpdateView,
    AcolhidoInativacaoView,
    InstituicaoListView,
    InstituicaoCreateView,
    InstituicaoUpdateView,
    InstituicaoInativacaoView,
    InstituicaoAtivacaoView,
    AcolhidoAtivacaoView,
)

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from vagas.views import InstituicaoViewSet, AcolhidoViewSet

router = DefaultRouter()
router.register(r'instituicoes-api', InstituicaoViewSet)
router.register(r'acolhidos-api', AcolhidoViewSet)

urlpatterns = [
    path('api/', include(router.urls)),

    path('admin/', admin.site.urls),
    #rotas para Acolhidos
    path('acolhidos/', AcolhidoListView.as_view(), name='acolhido_list'),
    path('acolhidos/create/', AcolhidoCreateView.as_view(), name='acolhido_create'),
    path('acolhidos/<int:pk>/update/', AcolhidoUpdateView.as_view(), name='acolhido_update'),
    path('acolhidos/<int:pk>/inativar/', AcolhidoInativacaoView.as_view(), name='acolhido_inativar'),
    #rotas para Instituicoes genéricas
    path('instituicoes/', InstituicaoListView.as_view(), name='instituicao_list'),
    path('instituicoes/create/', InstituicaoCreateView.as_view(), name='instituicao_create'),
    path('instituicoes/<int:pk>/update/', InstituicaoUpdateView.as_view(), name='instituicao_update'),
    path('instituicoes/<int:pk>/inativar/', InstituicaoInativacaoView.as_view(), name='instituicao_inativar'),
    path('instituicoes/<int:pk>/ativar/', InstituicaoAtivacaoView.as_view(), name='instituicao_ativar'),
    path('acolhidos/<int:pk>/ativar/', AcolhidoAtivacaoView.as_view(), name='acolhido_ativar'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout')
]
