from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseRedirect 

from rest_framework import viewsets, generics, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from .forms import InstituicaoForm
from .models import Acolhido, Instituicao, Categoria
from .serializers import InstituicaoSerializer, AcolhidoSerializer, CategoriaSerializer
from .forms import AcolhidoForm, DocumentacaoForm, EnderecoForm, InstituicaoForm, EnderecoInstituicaoForm, ContatoInstituicaoForm, CategoriaForm


# Para segurança------------------------------------------------------
class GroupRequiredMixin(UserPassesTestMixin):
    allowed_groups = []

    def test_func(self):
        # Superusuários sempre passam
        if self.request.user.is_superuser:
            return True
        # Verifica se o usuário pertence a um dos grupos permitidos
        return self.request.user.groups.filter(name__in=self.allowed_groups).exists()
    
#  APIs para o React----------------------------------------------------

class InstituicaoViewSet(viewsets.ModelViewSet):
   
    queryset = Instituicao.objects.all()
    serializer_class = InstituicaoSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    
    # Filtros de Busca 
    filter_backends = [filters.SearchFilter]
    search_fields = ['^nome', 'cnpj']


class AcolhidoViewSet(viewsets.ModelViewSet):
   
    queryset = Acolhido.objects.all()
    serializer_class = AcolhidoSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    # Filtros de Busca 
    filter_backends = [filters.SearchFilter]
    search_fields = ['nome', 'cpf']

class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer

# CRUD PARA ACOLHIDO--------------------------------------------------------
#1 - Listagem de Acolhidos
class AcolhidoListView(LoginRequiredMixin, GroupRequiredMixin, ListView):
    model = Acolhido
    template_name = 'acolhido_list.html'
    context_object_name = 'acolhidos'
    allowed_groups = ['Assistente de Campo', 'Secretaria Social']
    
    # filtro RF08
    def get_queryset(self):
        nome_filtro = self.request.GET.get('nome')
        if nome_filtro:
            return Acolhido.objects.filter(nome__icontains=nome_filtro)
        return Acolhido._base_manager.all()

#2 - Criação de Acolhidos
class AcolhidoCreateView(LoginRequiredMixin, GroupRequiredMixin, CreateView):
    model = Acolhido
    form_class = AcolhidoForm
    template_name = 'acolhido_form.html'
    success_url = reverse_lazy('acolhido_list')
    allowed_groups = ['Assistente de Campo', 'Secretaria Social']

    # 1. Enviamos os 3 formulários para o HTML
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['form_documentacao'] = DocumentacaoForm(self.request.POST)
            context['form_endereco'] = EnderecoForm(self.request.POST)
        else:
            context['form_documentacao'] = DocumentacaoForm()
            context['form_endereco'] = EnderecoForm()
        return context

    # 2. Interceptamos o momento de salvar
    def form_valid(self, form):
        context = self.get_context_data()
        form_documentacao = context['form_documentacao']
        form_endereco = context['form_endereco']

        # Só salva se todos os três estiverem corretos
        if form_documentacao.is_valid() and form_endereco.is_valid():
            documentacao = form_documentacao.save()
            endereco = form_endereco.save()
            
            # Segura o Acolhido na memória, anexa as chaves e salva no banco
            self.object = form.save(commit=False)
            self.object.documentacao = documentacao
            self.object.endereco = endereco
            self.object.save()
            
            messages.success(self.request, 'Acolhido cadastrado com sucesso!')
            return redirect(self.get_success_url())
        else:
            # Se der erro, devolve para a tela com as mensagens de erro
            return self.render_to_response(self.get_context_data(form=form))  

#3 - Edição de Acolhidos
class AcolhidoUpdateView(LoginRequiredMixin, GroupRequiredMixin, UpdateView):
    model = Acolhido
    form_class = AcolhidoForm
    template_name = 'acolhido_form.html'
    success_url = reverse_lazy('acolhido_list')
    allowed_groups = ['Assistente de Campo', 'Secretaria Social']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Como é edição, já temos o Acolhido (self.object). 
        # Pegamos a documentação e endereço dele (se existirem)
        doc_instance = getattr(self.object, 'documentacao', None)
        end_instance = getattr(self.object, 'endereco', None)

        if self.request.POST:
            context['form_documentacao'] = DocumentacaoForm(self.request.POST, instance=doc_instance)
            context['form_endereco'] = EnderecoForm(self.request.POST, instance=end_instance)
        else:
            context['form_documentacao'] = DocumentacaoForm(instance=doc_instance)
            context['form_endereco'] = EnderecoForm(instance=end_instance)
        
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        form_documentacao = context['form_documentacao']
        form_endereco = context['form_endereco']

        if form_documentacao.is_valid() and form_endereco.is_valid():
            # Aqui é mais simples: como as instâncias já existem, o save() vai dar um UPDATE no banco
            doc_obj = form_documentacao.save()
            end_obj = form_endereco.save()
            
            # Se o acolhido antigo por algum motivo não tinha endereço vinculado, vinculamos agora
            self.object = form.save(commit=False)
            self.object.documentacao = doc_obj
            self.object.endereco = end_obj
            self.object.save()

            messages.success(self.request, 'Cadastro atualizado com sucesso!')
            return super().form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form))

#4 - Inativação de Acolhidos
# Para converter o delete em inativar atraves de False, mantendo o registro no banco de dados, de acordo com o documento de requisitos.
class AcolhidoInativacaoView(LoginRequiredMixin, GroupRequiredMixin, UpdateView):
    model = Acolhido
    template_name = 'acolhido_confirm_inativacao.html'
    success_url = reverse_lazy('acolhido_list')
    fields = []
    allowed_groups = ['Assistente de Campo', 'Secretaria Social']

    def get_queryset(self):
        return Acolhido._base_manager.all()

    def post(self, request):
        self.object = self.get_object()
        self.object.ativo = False
        self.object.save()
        messages.success(request, f'Acolhido "{self.object.nome}" inativado com sucesso.')
        return redirect('acolhido_list')
        
#5 - Reativação de Acolhidos
class AcolhidoAtivacaoView(LoginRequiredMixin, GroupRequiredMixin, UpdateView):
    model = Acolhido
    template_name = 'acolhido_confirm_ativacao.html'
    success_url = reverse_lazy('acolhido_list')
    fields = []
    allowed_groups = ['Assistente de Campo', 'Secretaria Social']

    def get_queryset(self):
        return Acolhido._base_manager.all()

    # Apenas muda para True.
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.ativo = True
        self.object.save()
        messages.success(request, f'Acolhido "{self.object.nome}" reativado com sucesso!')
        return redirect('acolhido_list')

#CRUD PARA INSTITUIÇÃO-------------------------------------------------------
#6 - Listagem de Instituições
class InstituicaoListView(LoginRequiredMixin, GroupRequiredMixin, ListView):
    model = Instituicao
    template_name = 'instituicao_list.html'
    context_object_name = 'instituicoes'
    allowed_groups = ['Assistente de Campo', 'Secretaria Social']

    def get_queryset(self):
        nome_filtro = self.request.GET.get('nome')
        if nome_filtro:
            return Instituicao.objects.filter(nome__icontains=nome_filtro)
        return Instituicao._base_manager.all()
    
#7 - Criação de Instituições
class InstituicaoCreateView(LoginRequiredMixin, GroupRequiredMixin, CreateView):
    model = Instituicao
    form_class = InstituicaoForm
    template_name = 'instituicao_form.html'
    success_url = reverse_lazy('instituicao_list')
    allowed_groups = ['Gestor Central', 'Administrador'] # Ajuste para os seus grupos

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['form_endereco'] = EnderecoInstituicaoForm(self.request.POST)
            context['form_contato'] = ContatoInstituicaoForm(self.request.POST)
        else:
            context['form_endereco'] = EnderecoInstituicaoForm()
            context['form_contato'] = ContatoInstituicaoForm()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        form_endereco = context['form_endereco']
        form_contato = context['form_contato']

        if form_endereco.is_valid() and form_contato.is_valid():
            # 1. Salva o endereço (Relacionamento 1 para 1)
            endereco = form_endereco.save()
            
            # 2. Segura a Instituição na memória e vincula o endereço
            self.object = form.save(commit=False)
            self.object.endereco = endereco
            self.object.save()
            
            # 3. Salva o contato vinculando-o à Instituição recém-criada (Relacionamento 1 para N)
            contato = form_contato.save(commit=False)
            contato.instituicao = self.object
            contato.save()
            
            messages.success(self.request, 'Unidade cadastrada com sucesso!')
            return redirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))
#8 - Edição de Instituições
class InstituicaoUpdateView(LoginRequiredMixin, GroupRequiredMixin, UpdateView):
    model = Instituicao
    form_class = InstituicaoForm
    template_name = 'instituicao_form.html'
    success_url = reverse_lazy('instituicao_list')
    allowed_groups = ['Gestor Central', 'Administrador']

    # 1. Enviamos os formulários para o HTML, mas agora PREENCHIDOS
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Puxamos o endereço que já está salvo na instituição atual
        end_instance = getattr(self.object, 'endereco', None)
        
        # Como o relacionamento de contato é 1 para N (uma lista), 
        # nós pegamos o primeiro contato cadastrado (o principal) usando .first()
        contato_instance = self.object.contato.first()

        if self.request.POST:
            # Se for POST (botão salvar clicado), injetamos os dados novos por cima da instância antiga
            context['form_endereco'] = EnderecoInstituicaoForm(self.request.POST, instance=end_instance)
            context['form_contato'] = ContatoInstituicaoForm(self.request.POST, instance=contato_instance)
        else:
            # Se for GET (apenas abriu a tela), desenhamos o form com a instância antiga
            context['form_endereco'] = EnderecoInstituicaoForm(instance=end_instance)
            context['form_contato'] = ContatoInstituicaoForm(instance=contato_instance)
            
        return context

    # 2. Interceptamos o salvamento
    def form_valid(self, form):
        context = self.get_context_data()
        form_endereco = context['form_endereco']
        form_contato = context['form_contato']

        # Verifica se não há erros de digitação (ex: CEP com letras)
        if form_endereco.is_valid() and form_contato.is_valid():
            
            # O .save() aqui é inteligente. Como usamos o 'instance' lá em cima, 
            # ele sabe que deve atualizar a linha existente no PostgreSQL em vez de criar uma nova.
            endereco = form_endereco.save()
            
            # Salva as alterações da Instituição e garante o vínculo do endereço
            self.object = form.save(commit=False)
            self.object.endereco = endereco
            self.object.save()
            
            # Salva as alterações do Contato
            contato = form_contato.save(commit=False)
            contato.instituicao = self.object
            contato.save()
            
            messages.success(self.request, 'Unidade atualizada com sucesso!')
            # Retorna o form_valid padrão do UpdateView
            return super().form_valid(form) 
        else:
            # Devolve para a tela com os avisos em vermelho se houver erro
            return self.render_to_response(self.get_context_data(form=form))
    
#9 - Inativação de Instituições
class InstituicaoInativacaoView(LoginRequiredMixin, GroupRequiredMixin, UpdateView):
    model = Instituicao
    template_name = 'instituicao_confirm_inativacao.html'
    success_url = reverse_lazy('instituicao_list')
    fields = []
    allowed_groups = ['Secretaria Social']

    def get_queryset(self):
        return Instituicao._base_manager.all()

    # Mesma ideia do acolhido, mas com a validação adicional para verificar se existem acolhidos ativos vinculados à instituição.
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
class InstituicaoAtivacaoView(LoginRequiredMixin, GroupRequiredMixin, UpdateView):
    model = Instituicao
    template_name = 'instituicao_confirm_ativacao.html'
    success_url = reverse_lazy('instituicao_list')
    fields = []
    allowed_groups = ['Secretaria Social']

    def get_queryset(self):
        return Instituicao._base_manager.all()

    # Apenas muda para True.
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.ativo = True
        self.object.save()

        messages.success(request, f'Instituição "{self.object.nome}" reativada com sucesso!')
        return redirect('instituicao_list')

class CategoriaCreateView(LoginRequiredMixin, GroupRequiredMixin, CreateView):
    model = Categoria
    form_class = CategoriaForm
    template_name = 'categoria_form.html'
    success_url = reverse_lazy('instituicao_list')
    allowed_groups = ['Gestor Central', 'Administrador']

    def form_valid(self, form):
        messages.success(self.request, 'Nova categoria institucional cadastrada com sucesso!')
        return super().form_valid(form)