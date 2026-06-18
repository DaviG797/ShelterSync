import re
from rest_framework import serializers
from .models import Acolhido, Documentacao, Endereco_Acolhido
from .models import Instituicao, Categoria, Endereco_Instituicao,  Contato_Instituicao

def cpf_e_valido(cpf):
    cpf = re.sub(r'\D', '', str(cpf))
    if len(cpf) != 11 or len(set(cpf)) == 1:
        return False
    
    for i in range(9, 11):
        soma = sum(int(cpf[num]) * ((i + 1) - num) for num in range(0, i))
        digito = ((soma * 10) % 11) % 10
        if digito != int(cpf[i]):
            return False
    return True

class EnderecoAcolhidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Endereco_Acolhido
        fields = ['id', 'situacao_rua', 'cep', 'logradouro', 'numero']

class DocumentacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Documentacao
        fields = ['id', 'tipo', 'numero', 'justificativa']

    # O método 'validate' roda automaticamente antes de salvar no banco
    def validate(self, dados):
        tipo = dados.get('tipo')
        numero = dados.get('numero', '')
        justificativa = dados.get('justificativa', '')

        if tipo == 'SEM_DOC':
            if not justificativa:
                raise serializers.ValidationError({"justificativa": "A justificativa é obrigatória para pessoas sem documentação."})
            dados['numero'] = None # Garante que o banco receba nulo, ativando a nossa regra de UniqueConstraint

        elif tipo == 'CPF':
            if not numero or not cpf_e_valido(numero):
                raise serializers.ValidationError({"numero": "O CPF informado é inválido."})

        elif tipo == 'RG':
            # O RG varia por estado no Brasil, então validamos se tem um tamanho razoável e caracteres alfanuméricos
            numero_limpo = re.sub(r'\W', '', str(numero))
            if not numero_limpo or len(numero_limpo) < 5:
                raise serializers.ValidationError({"numero": "O RG informado parece ser inválido."})
            dados['numero'] = numero_limpo # Salva limpo no banco

        return dados
    
class AcolhidoSerializer(serializers.ModelSerializer):
    # Avisamos que estes campos receberão objetos JSON inteiros do React
    documentacao = DocumentacaoSerializer()
    endereco = EnderecoAcolhidoSerializer()

    class Meta:
        model = Acolhido
        fields = [
            'id', 'nome', 'data_nascimento', 'documentacao', 'nome_mae', 'nome_pai', 
            'familiares', 'endereco', 'renda', 'genero', 'orientacao_sexual', 
            'laudo_medico', 'motivo_acolhimento', 'ativo', 'instituicao_atual'
        ]

    # Substituímos o método de criação padrão para ensinar o Django a salvar em 3 tabelas
    def create(self, validated_data):
        # 1. Retiramos os dados aninhados do pacote principal
        dados_documentacao = validated_data.pop('documentacao', None)
        dados_endereco = validated_data.pop('endereco', None)

        # 2. Criamos as linhas nas tabelas de apoio primeiro
        documentacao_obj = None
        if dados_documentacao:
            documentacao_obj = Documentacao.objects.create(**dados_documentacao)

        endereco_obj = None
        if dados_endereco:
            endereco_obj = Endereco_Acolhido.objects.create(**dados_endereco)

        # 3. Criamos o Acolhido e colamos os IDs dos objetos criados acima
        acolhido = Acolhido.objects.create(
            documentacao=documentacao_obj,
            endereco=endereco_obj,
            **validated_data
        )

        return acolhido
    
class AcolhidoResumoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Acolhido
        fields = ['id', 'nome', 'genero', 'data_nascimento', 'ativo']

# Serializer Instituição -------------------------------------------------
class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ['id', 'nome', 'descricao']

class EnderecoInstituicaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Endereco_Instituicao
        fields = ['id', 'rua', 'numero', 'bairro', 'cidade', 'estado', 'cep']

class ContatoInstituicaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contato_Instituicao
        # Não colocamos a 'instituicao' aqui, pois o Django vai preencher isso sozinho
        fields = ['id', 'tipo', 'valor']

class InstituicaoSerializer(serializers.ModelSerializer):
    # 1 para 1: Um único objeto de endereço
    endereco = EnderecoInstituicaoSerializer()
    
    # 1 para N: Uma LISTA de contatos (Atenção ao many=True)
    contato = ContatoInstituicaoSerializer(many=True, required=False) 
    
    # Campo extra de leitura para o React mostrar o nome bonito da categoria nos cartões
    nome_categoria = serializers.CharField(source='categorizacao.nome', read_only=True)

    acolhidos = AcolhidoResumoSerializer(many=True, read_only=True)

    vagas_disponiveis = serializers.ReadOnlyField()

    class Meta:
        model = Instituicao
        fields = [
            'id', 'nome', 'cnpj', 'capacidade_total', 'vagas_disponiveis', 'ativo', 
            'categorizacao', 'nome_categoria', 'endereco', 'contato', 'acolhidos'
        ]

    # A MÁGICA: Salvando em 3 tabelas diferentes ao mesmo tempo
    def create(self, validated_data):
        # 1. Extraímos os dados que vão para as outras tabelas
        dados_endereco = validated_data.pop('endereco', None)
        dados_contatos = validated_data.pop('contato', []) # Puxa como uma lista vazia se não vier nada

        # 2. Criamos o endereço primeiro (se existir)
        endereco_obj = None
        if dados_endereco:
            endereco_obj = Endereco_Instituicao.objects.create(**dados_endereco)

        # 3. Criamos a Instituição, vinculando o endereço criado acima
        instituicao = Instituicao.objects.create(
            endereco=endereco_obj,
            **validated_data
        )

        # 4. Criamos os contatos usando um loop (pois podem ser vários)
        for dado_contato in dados_contatos:
            Contato_Instituicao.objects.create(
                instituicao=instituicao, # Aqui dizemos de quem é esse contato!
                **dado_contato
            )

        return instituicao
    
class InstituicaoResumoSerializer(serializers.ModelSerializer):

    vagas_disponiveis = serializers.ReadOnlyField()

    class Meta:
        model = Instituicao
        fields =[
            'id','nome', 'cnpj', 'capacidade_total',
            'vagas_disponiveis', 'categoria', 'ativo'
        ]