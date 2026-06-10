from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from .models import Acolhido, Instituicao
from .forms import AcolhidoForm, InstituicaoForm
from django.http import HttpResponseRedirect #está aqui para caos seja preciso.
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

class GroupRequiredMixin(UserPassesTestMixin):
    allowed_groups = []

    def test_func(self):
        # Superusuários sempre passam
        if self.request.user.is_superuser:
            return True
        # Verifica se o usuário pertence a um dos grupos permitidos
        return self.request.user.groups.filter(name__in=self.allowed_groups).exists()

# CRUD PARA ACOLHIDO--------------------------------------------------------
#1 - Listagem de Acolhidos
class AcolhidoListView(LoginRequiredMixin, GroupRequiredMixin, ListView):
    model = Acolhido
    template_name = 'acolhido_list.html'
    context_object_name = 'acolhidos'
    # filtro RF08
    def get_queryset(self):
        nome_filtro = self.request.GET.get('nome')
        if nome_filtro:
            return Acolhido.objects.filter(nome__icontains=nome_filtro)
        return Acolhido._base_manager.all()
    allowed_groups = ['Assistente de Campo', 'Secretaria Social']

#2 - Criação de Acolhidos
class AcolhidoCreateView(LoginRequiredMixin, GroupRequiredMixin, CreateView):
    model = Acolhido
    form_class = AcolhidoForm
    template_name = 'acolhido_form.html'
    success_url = reverse_lazy('acolhido_list')
    allowed_groups = ['Assistente de Campo', 'Secretaria Social']

#3 - Edição de Acolhidos
class AcolhidoUpdateView(LoginRequiredMixin, GroupRequiredMixin, UpdateView):
    model = Acolhido
    form_class = AcolhidoForm
    template_name = 'acolhido_form.html'
    success_url = reverse_lazy('acolhido_list')
    allowed_groups = ['Assistente de Campo', 'Secretaria Social']

#4 - Inativação de Acolhidos
# Para converter o delete em inativar atraves de False, mantendo o registro no banco de dados, de acordo com o documento de requisitos.
class AcolhidoInativacaoView(LoginRequiredMixin, GroupRequiredMixin, UpdateView):
    model = Acolhido
    template_name = 'acolhido_confirm_inativacao.html'
    success_url = reverse_lazy('acolhido_list')
    fields = []

    def get_queryset(self):
        return Acolhido._base_manager.all()

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        # faz a inativação
        self.object.ativo = False
        self.object.save()

        messages.success(request, f'Acolhido "{self.object.nome}" inativado com sucesso.')
        return redirect('acolhido_list')
    allowed_groups = ['Assistente de Campo', 'Secretaria Social']
        
#5 - Reativação de Acolhidos
class AcolhidoAtivacaoView(LoginRequiredMixin, GroupRequiredMixin, UpdateView):
    model = Acolhido
    template_name = 'acolhido_confirm_ativacao.html'
    success_url = reverse_lazy('acolhido_list')
    fields = []

    def get_queryset(self):
        return Acolhido._base_manager.all()

    #Apenas muda para True.
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.ativo = True
        self.object.save()
        messages.success(request, f'Acolhido "{self.object.nome}" reativado com sucesso!')
        return redirect('acolhido_list')
    allowed_groups = ['Assistente de Campo', 'Secretaria Social']


#CRUD PARA INSTITUIÇÃO-------------------------------------------------------
#6 - Listagem de Instituições
class InstituicaoListView(LoginRequiredMixin, GroupRequiredMixin, ListView):
    model = Instituicao
    template_name = 'instituicao_list.html'
    context_object_name = 'instituicoes'
    # filtro RF08
    def get_queryset(self):
        nome_filtro = self.request.GET.get('nome')
        if nome_filtro:
            return Instituicao.objects.filter(nome__icontains=nome_filtro)
        return Instituicao._base_manager.all()
    allowed_groups = ['Assistente de Campo', 'Secretaria Social']
    
#7 - Criação de Instituições
class InstituicaoCreateView(LoginRequiredMixin, GroupRequiredMixin, CreateView):
    model = Instituicao
    form_class = InstituicaoForm
    template_name = 'instituicao_form.html'
    success_url = reverse_lazy('instituicao_list')
    allowed_groups = ['Secretaria Social']

#8 - Edição de Instituições
class InstituicaoUpdateView(LoginRequiredMixin, GroupRequiredMixin, UpdateView):
    model = Instituicao
    form_class = InstituicaoForm
    template_name = 'instituicao_form.html'
    success_url = reverse_lazy('instituicao_list')
    allowed_groups = ['Secretaria Social']
    
#9 - Inativação de Instituições
class InstituicaoInativacaoView(LoginRequiredMixin, GroupRequiredMixin, UpdateView):
    model = Instituicao
    template_name = 'instituicao_confirm_inativacao.html'
    success_url = reverse_lazy('instituicao_list')
    fields = []

    def get_queryset(self):
        return Instituicao._base_manager.all()

    #mesma ideia do acolhido, mas com a validação adicional para verificar se existem acolhidos ativos vinculados à instituição.
    def post(self, request, *args, **kwargs):
            self.object = self.get_object()

            vagas_ocupadas = Acolhido.objects.filter(instituicao_atual=self.object, ativo=True).count()
            if vagas_ocupadas > 0:
                messages.error(request, f'Não é possível inativar a instituição "{self.object.nome}", pois existem {vagas_ocupadas} acolhidos ativos vinculados a ela.')
                return redirect('instituicao_list')
            # faz a inativação
            self.object.ativo = False
            self.object.save()

            messages.success(request, f'Instituição "{self.object.nome}" inativada com sucesso.')
            return redirect('instituicao_list')
    allowed_groups = ['Secretaria Social']

#10 - Reativação de Instituições
class InstituicaoAtivacaoView(LoginRequiredMixin, GroupRequiredMixin, UpdateView):
    model = Instituicao
    template_name = 'instituicao_confirm_ativacao.html'
    success_url = reverse_lazy('instituicao_list')
    fields = []

    def get_queryset(self):
        return Instituicao._base_manager.all()

    #Apenas muda para True.
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.ativo = True
        self.object.save()

        messages.success(request, f'Instituição "{self.object.nome}" reativada com sucesso!')
        return redirect('instituicao_list')
    allowed_groups = ['Secretaria Social']