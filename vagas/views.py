from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from .models import Acolhido, Instituicao
from .forms import AcolhidoForm, InstituicaoForm
from django.http import HttpResponseRedirect #está aqui para caos seja preciso.
from django.shortcuts import redirect
from django.contrib import messages


# CRUD PARA ACOLHIDO--------------------------------------------------------
#1 - Listagem de Acolhidos
class AcolhidoListView(ListView):
    model = Acolhido
    template_name = 'acolhido_list.html'
    context_object_name = 'acolhidos'
    # filtro RF08
    def get_queryset(self):
        nome_filtro = self.request.GET.get('nome')
        if nome_filtro:
            return Acolhido.objects.filter(nome__icontains=nome_filtro)
        return Acolhido._base_manager.all()

#2 - Criação de Acolhidos
class AcolhidoCreateView(CreateView):
    model = Acolhido
    form_class = AcolhidoForm
    template_name = 'acolhido_form.html'
    success_url = reverse_lazy('acolhido_list')

#3 - Edição de Acolhidos
class AcolhidoUpdateView(UpdateView):
    model = Acolhido
    form_class = AcolhidoForm
    template_name = 'acolhido_form.html'
    success_url = reverse_lazy('acolhido_list')

#4 - Inativação de Acolhidos
# Para converter o delete em inativar atraves de False, mantendo o registro no banco de dados, de acordo com o documento de requisitos.
class AcolhidoInativacaoView(UpdateView):
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
        
#5 - Reativação de Acolhidos
class AcolhidoAtivacaoView(UpdateView):
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


#CRUD PARA INSTITUIÇÃO-------------------------------------------------------
#6 - Listagem de Instituições
class InstituicaoListView(ListView):
    model = Instituicao
    template_name = 'instituicao_list.html'
    context_object_name = 'instituicoes'
    # filtro RF08
    def get_queryset(self):
        nome_filtro = self.request.GET.get('nome')
        if nome_filtro:
            return Instituicao.objects.filter(nome__icontains=nome_filtro)
        return Instituicao._base_manager.all()
    
#7 - Criação de Instituições
class InstituicaoCreateView(CreateView):
    model = Instituicao
    form_class = InstituicaoForm
    template_name = 'instituicao_form.html'
    success_url = reverse_lazy('instituicao_list')

#8 - Edição de Instituições
class InstituicaoUpdateView(UpdateView):
    model = Instituicao
    form_class = InstituicaoForm
    template_name = 'instituicao_form.html'
    success_url = reverse_lazy('instituicao_list')
    
#9 - Inativação de Instituições
class InstituicaoInativacaoView(UpdateView):
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

#10 - Reativação de Instituições
class InstituicaoAtivacaoView(UpdateView):
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