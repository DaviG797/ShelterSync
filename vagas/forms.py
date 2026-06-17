from django import forms
from .models import Acolhido, Documentacao, Endereco_Acolhido , Instituicao, Endereco_Instituicao, Contato_Instituicao, Categoria

# Forms para os modelos Acolhido e Instituição, utilizando ModelForm para facilitar a criação de formulários baseados nos modelos definidos.
# O campo 'fields' com valor '__all__' indica que todos os campos do modelo serão incluídos no formulário.

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nome', 'descricao']
        widgets = {
            'descricao': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Breve descrição do perfil de atendimento...'}),
        }

class AcolhidoForm(forms.ModelForm):
    class Meta:
        model = Acolhido
        fields = '__all__'

class InstituicaoForm(forms.ModelForm):
    class Meta:
        model = Instituicao
        fields = '__all__'

class DocumentacaoForm(forms.ModelForm):
    class Meta:
        model = Documentacao
        fields = ['tipo', 'numero', 'justificativa']

class EnderecoForm(forms.ModelForm):
    class Meta:
        model = Endereco_Acolhido
        fields = ['situacao_rua', 'cep', 'logradouro', 'numero']

class AcolhidoForm(forms.ModelForm):
    class Meta:
        model = Acolhido
        # Repare que tiramos 'documentacao' e 'endereco' daqui, 
        # pois eles têm seus próprios formulários acima.
        fields = [
            'nome', 'data_nascimento', 'nome_mae', 'nome_pai', 
            'familiares', 'renda', 'genero', 'orientacao_sexual', 
            'laudo_medico', 'motivo_acolhimento', 'instituicao_atual'
        ]

class EnderecoInstituicaoForm(forms.ModelForm):
    class Meta:
        model = Endereco_Instituicao
        fields = ['cep', 'rua', 'numero', 'bairro', 'cidade', 'estado']

class ContatoInstituicaoForm(forms.ModelForm):
    class Meta:
        model = Contato_Instituicao
        # Removemos 'instituicao' daqui, pois o vínculo será feito automaticamente na View
        fields = ['tipo', 'valor']

class InstituicaoForm(forms.ModelForm):
    class Meta:
        model = Instituicao
        # O 'endereco' fica de fora, pois é tratado no formulário acima
        fields = ['nome', 'cnpj', 'capacidade_total', 'categorizacao', 'ativo']