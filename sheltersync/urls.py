"""
URL configuration for sheltersync.
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views as token_views

from vagas.views import InstituicaoViewSet, AcolhidoViewSet, CategoriaViewSet, CategoriaCreateView

from django.contrib.auth import views as auth_views
from vagas.views import (
    AcolhidoListView, AcolhidoCreateView, AcolhidoUpdateView, AcolhidoInativacaoView,
    InstituicaoListView, InstituicaoCreateView, InstituicaoUpdateView,
    InstituicaoInativacaoView, InstituicaoAtivacaoView, AcolhidoAtivacaoView,
)

router = DefaultRouter()
router.register(r'instituicoes-api', InstituicaoViewSet, basename='instituicao')
router.register(r'acolhidos-api', AcolhidoViewSet, basename='acolhido')
router.register(r'categorias', CategoriaViewSet, basename='categoria')

urlpatterns = [
    # Rota padrão do painel de administração
    path('admin/', admin.site.urls),

    # Rotas utilizadas pelo React ---------------------------
    path('api/', include(router.urls)),
    path('api/token/', token_views.obtain_auth_token),

    # Rotas usada pelo back ---------------------------------
    
    # -- Rotas de Acolhidos --
    path('acolhidos/', AcolhidoListView.as_view(), name='acolhido_list'),
    path('acolhidos/create/', AcolhidoCreateView.as_view(), name='acolhido_create'),
    path('acolhidos/<int:pk>/update/', AcolhidoUpdateView.as_view(), name='acolhido_update'),
    path('acolhidos/<int:pk>/inativar/', AcolhidoInativacaoView.as_view(), name='acolhido_inativar'),
    path('acolhidos/<int:pk>/ativar/', AcolhidoAtivacaoView.as_view(), name='acolhido_ativar'),
    
    # -- Rotas de Instituições --
    path('instituicoes/', InstituicaoListView.as_view(), name='instituicao_list'),
    path('instituicoes/create/', InstituicaoCreateView.as_view(), name='instituicao_create'),
    path('instituicoes/<int:pk>/update/', InstituicaoUpdateView.as_view(), name='instituicao_update'),
    path('instituicoes/<int:pk>/inativar/', InstituicaoInativacaoView.as_view(), name='instituicao_inativar'),
    path('instituicoes/<int:pk>/ativar/', InstituicaoAtivacaoView.as_view(), name='instituicao_ativar'),
    
    # -- Sistema de Login Clássico --
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('categorias/create/', CategoriaCreateView.as_view(), name='categoria_create')
]