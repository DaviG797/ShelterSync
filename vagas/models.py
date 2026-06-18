from django.db import models
from django.db.models import Q
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.utils import timezone

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
    endereco = models.OneToOneField( # D-13 (Endereço completo da instituicao)
        Endereco_Instituicao, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )

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

# Para gerar um histórico de entrada e saida para relatorios
class HistoricoAcolhimento(models.Model):
    acolhido = models.ForeignKey(
        Acolhido, 
        on_delete=models.CASCADE, 
        related_name='historico_estadias'
    )
    instituicao = models.ForeignKey(
        Instituicao, 
        on_delete=models.CASCADE, 
        related_name='historico_vagas'
    )
    
    # Grava a data e hora exata em que o registro foi criado
    data_entrada = models.DateTimeField(default=timezone.now) 
    
    # Fica em branco até o dia em que ele sair do abrigo
    data_saida = models.DateTimeField(null=True, blank=True) 
    
    motivo_saida = models.CharField(max_length=200, blank=True, null=True) 

    def __str__(self):
        return f"{self.acolhido.nome} -> {self.instituicao.nome}"

# Para criar as reservas -------------------------------------------
class ReservaVaga(models.Model):
    acolhido = models.OneToOneField(
        Acolhido, 
        on_delete=models.CASCADE, 
        related_name='reserva_atual'
    )
    instituicao = models.ForeignKey(
        Instituicao, 
        on_delete=models.CASCADE, 
        related_name='fila_espera'
    )
    
    # Grava o milissegundo exato em que a pessoa entrou na fila
    data_solicitacao = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Organiza automaticamente a tabela para que o mais antigo fique no topo (índice 0)
        ordering = ['data_solicitacao'] 

    def __str__(self):
        return f"Reserva: {self.acolhido.nome} aguardando vaga em {self.instituicao.nome}"
    
# Garantir o histórico conforme o acolhido esteja vinculado a uma instituição 
  
# ANTES DE SALVAR (Descobre de onde ele está saindo)
@receiver(pre_save, sender=Acolhido)
def fechar_historico_antigo(sender, instance, **kwargs):
    if instance.pk: # Se o acolhido já existe no banco
        acolhido_antigo = Acolhido.objects.get(pk=instance.pk)
        
        # Se a instituição mudou (ou se ele saiu do sistema)
        if acolhido_antigo.instituicao_atual != instance.instituicao_atual:
            if acolhido_antigo.instituicao_atual:
                # Procura o histórico em aberto e preenche a data de saída com o dia de hoje
                historico_aberto = HistoricoAcolhimento.objects.filter(
                    acolhido=instance, 
                    instituicao=acolhido_antigo.instituicao_atual, 
                    data_saida__isnull=True
                ).first()
                
                if historico_aberto:
                    historico_aberto.data_saida = timezone.now()
                    historico_aberto.motivo_saida = "Transferência ou Desligamento"
                    historico_aberto.save()

#  DEPOIS DE SALVAR (Registra onde ele está entrando)
@receiver(post_save, sender=Acolhido)
def criar_novo_historico(sender, instance, created, **kwargs):

    # Se ele foi alocado em uma instituição
    if instance.instituicao_atual:
        # Verifica se já não existe um histórico em aberto para ele nesse mesmo abrigo
        historico_aberto_existe = HistoricoAcolhimento.objects.filter(
            acolhido=instance,
            instituicao=instance.instituicao_atual,
            data_saida__isnull=True
        ).exists()

        if not historico_aberto_existe:
            # Cria a nova página no Livro de Registros!
            HistoricoAcolhimento.objects.create(
                acolhido=instance,
                instituicao=instance.instituicao_atual,
                data_entrada=timezone.now()
            )



# Modelo para o Histórico da Instituição
class HistoricoInstituicao(models.Model):
    instituicao = models.ForeignKey(
        Instituicao,
        on_delete=models.CASCADE,
        related_name='historico_alteracoes'
    )

    # Registra o que mudou
    capacidade_anterior = models.PositiveIntegerField(null=True, blank=True)
    capacidade_nova = models.PositiveIntegerField()

    status_anterior = models.BooleanField(null=True, blank=True)
    status_novo = models.BooleanField()

    # Data exata em que a mudança ocorreu
    data_alteracao = models.DateTimeField(default=timezone.now)

    #"Aumento de vagas" ou "Instituição temporariamente fechada"
    motivo_alteracao = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f"Alteração em {self.instituicao.nome} - {self.data_alteracao.strftime('%d/%m/%Y')}"


# ANTES DE SALVAR (Verifica o que mudou na instituição e gera o registro)
@receiver(pre_save, sender=Instituicao)
def registrar_historico_instituicao(sender, instance, **kwargs):
    if instance.pk:  # Verifica se a instituição já existe no banco (não é um cadastro novo)
        try:
            # Busca os dados antigos da instituição antes de salvar a nova versão
            instituicao_antiga = sender.objects.get(pk=instance.pk)

            # Verifica se a capacidade de vagas OU o status (ativo/inativo) mudaram
            mudou_capacidade = instituicao_antiga.capacidade_vagas != instance.capacidade_vagas
            mudou_status = instituicao_antiga.ativo != instance.ativo

            if mudou_capacidade or mudou_status:
                # Cria a linha do tempo relatando a mudança
                HistoricoInstituicao.objects.create(
                    instituicao=instance,
                    capacidade_anterior=instituicao_antiga.capacidade_vagas,
                    capacidade_nova=instance.capacidade_vagas,
                    status_anterior=instituicao_antiga.ativo,
                    status_novo=instance.ativo,
                    motivo_alteracao="Atualização de cadastro (Capacidade/Status)"
                )
        except sender.DoesNotExist:
            pass

@receiver(pre_save, sender=Acolhido)
def processar_fila_de_espera(sender, instance, **kwargs):
    if instance.pk:
        acolhido_antigo = Acolhido.objects.get(pk=instance.pk)
        
        # Se o acolhido tinha uma instituição e agora está saindo dela
        if acolhido_antigo.instituicao_atual and acolhido_antigo.instituicao_atual != instance.instituicao_atual:
            
            instituicao_que_abriu_vaga = acolhido_antigo.instituicao_atual
            
            # Pega o PRIMEIRO da fila desta instituição específica
            proximo_da_fila = ReservaVaga.objects.filter(instituicao=instituicao_que_abriu_vaga).first()
            
            if proximo_da_fila:
                pessoa_esperando = proximo_da_fila.acolhido
                
                # Transfere a pessoa da fila para dentro da instituição
                pessoa_esperando.instituicao_atual = instituicao_que_abriu_vaga
                pessoa_esperando.save() # Salva a pessoa (isso também vai engatilhar o Histórico!)
                
                # Exclui a reserva temporária do banco, limpando a tabela
                proximo_da_fila.delete()