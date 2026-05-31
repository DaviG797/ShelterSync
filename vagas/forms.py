from django import forms
from .models import Acolhido, Instituicao

# Forms para os modelos Acolhido e Instituição, utilizando ModelForm para facilitar a criação de formulários baseados nos modelos definidos. O campo 'fields' com valor '__all__' indica que todos os campos do modelo serão incluídos no formulário.

class AcolhidoForm(forms.ModelForm):
    class Meta:
        model = Acolhido
        fields = '__all__'

class InstituicaoForm(forms.ModelForm):
    class Meta:
        model = Instituicao
        fields = '__all__'