from django.db import models
from django.db.models import Q

class Categoria(models.Model):

    nome = models.CharField(max_length=50, unique=True ) # Nome da categoria
    descricao = models.TextField(blank=True) # Descrição da categoria em texto longo

    def __str__(self):
        return self.nome

class Endereco_Instituicao(models.Model):

    rua = models.CharField(max_length=255)
    numero = models.CharField(max_length=10)
    bairro = models.CharField(max_length=25)
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=2) 
    cep = models.CharField(max_length=9)

    def __str__(self):
        return f"{self.rua}, {self.numero} - {self.cidade}/{self.estado}"

class Instituicao(models.Model):

    nome = models.CharField(max_length=100) # D-12 (Nome da instituicao)
    endereco = models.OneToOneField( # D-13 (Endereço completo da instituicao)
        Endereco_Instituicao, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    ) 
    capacidade_total = models.IntegerField() # D-14 (Capacidade de vagas)
    categorizacao = models.ForeignKey(
        Categoria, 
        on_delete=models.SET_NULL,
        null=True, 
        blank=True,
        related_name='instituicoes'
    )
    cnpj = models.CharField(max_length=18, unique=True) # D-16 + RN-10 ("unique" garante CNPJ único)
    ativo = models.BooleanField(default=True) # RF-07 (Inativar instituicao)

    @property
    def vagas_disponiveis(self): # Retorna a quantidade de vagas restantes em tempo real
        ocupadas = self.acolhidos.filter(ativo=True).count()

        vagas = self.capacidade_total - ocupadas

        return vagas if vagas > 0 else 0

    def __str__(self): # Retorna o nome da instituicao para não mostrar "instituicao object (1)" no admin.
        return self.nome
    
class Contato_Instituicao(models.Model): # D-17
    
    instituicao = models.ForeignKey(
        Instituicao,
        on_delete=models.CASCADE,
        related_name='contato'
    )

    tipo = models.CharField(max_length=10)
    valor = models.CharField(max_length=25)

    def __str__(self):
        return f"{self.tipo}: {self.valor}"
    
class Documentacao(models.Model):
    TIPO_DOC_CHOICES = [
        ('CPF', 'CPF'),
        ('RG', 'RG'),
        ('CNH', 'CNH'),
        ('SEM_DOC', 'Sem Documentação')
    ]
    
    tipo = models.CharField(max_length=10, choices=TIPO_DOC_CHOICES)
    
    numero = models.CharField(max_length=20, blank=True, null=True) # Guarda apenas os números puros do documento
    
    justificativa = models.TextField(blank=True, null=True) # Só será preenchida se o tipo for 'SEM_DOC'

    class Meta:

        # Aplicando regras de indice unico
        constraints = [
            models.UniqueConstraint(
                
                fields=['tipo', 'numero'], 
                
                condition=~Q(tipo='SEM_DOC'), 
                
                name='documento_unico_por_tipo'
            )
        ]

    def __str__(self):
        return f"{self.tipo}: {self.numero if self.numero else 'Sem documento'}"
    
class Endereco_Acolhido(models.Model):

    # Se for True, significa que é morador de rua
    situacao_rua = models.BooleanField(default=False) 
    
    # CEP é obrigatório (Se for morador de rua, usa o CEP geral da cidade)
    cep = models.CharField(max_length=9) 
    
    # Logradouro e Número podem ficar em branco se for morador de rua
    logradouro = models.CharField(max_length=200, blank=True, null=True)
    numero = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        if self.situacao_rua:
            return f"Situação de Rua - CEP Geral: {self.cep}"
        return f"{self.logradouro}, {self.numero} - CEP: {self.cep}"
    
class Acolhido(models.Model):

    nome = models.CharField(max_length=100) # D-01 (Nome do acolhido)
    data_nascimento = models.DateField() # D-03 (Data de nascimento do acolhido)
    documentacao = models.OneToOneField(
        Documentacao,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    ) # D-02 + RN-15 (Documentação do acolhido, ex: RG, CPF)
    
    nome_mae = models.CharField(max_length=150, blank=True, null=True) # D-06
    nome_pai = models.CharField(max_length=150, blank=True, null=True) # D-06
    familiares = models.TextField(blank=True, default="") # D-05 (Informações sobre familiares do acolhido para possível contato)

    endereco = models.OneToOneField(
        Endereco_Acolhido,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    ) # D-07 (Endereço completo do acolhido, se conhecido)
    
    renda = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True) # D-08 (Renda mensal do acolhido, se houver)

    genero = models.CharField(max_length=20) # D-04 (Gênero do acolhido)
    orientacao_sexual = models.CharField(max_length=30, blank=True, default="") # D-10 (Orientação sexual do acolhido, se conhecido)

    laudo_medico = models.FileField(upload_to='laudos_saude/', blank=True, null=True) # D-09 (Informações sobre histórico de saúde do acolhido)
    motivo_acolhimento = models.TextField() # D-11 (Motivo do acolhimento do indivíduo)
    
    ativo = models.BooleanField(default=True) # RF-02 (Inativar acolhido)

    instituicao_atual = models.ForeignKey(
        Instituicao,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='acolhidos'
    )

    def __str__(self): #Retorna o nome do acolhido para não mostrar "acolhido object (1)" no admin.
        return self.nome

