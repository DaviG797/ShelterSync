from django.db import models

class Instituicao(models.Model):
    nome = models.CharField(max_length=100) # D-12 (Nome da instituição)
    endereco = models.CharField(max_length=200) # D-13 (Endereço completo da instituição)
    capacidade_total = models.IntegerField() # D-14 (Capacidade de vagas)
    categorizacao = models.CharField(max_length=50) # D-15 (Perfil do abrigo, ex: "Abrigo para idosos".)
    cnpj = models.CharField(max_length=18, unique=True) # D-16 + RN-10 ("unique" garante CNPJ único)
    contato = models.CharField(max_length=20, blank=True, default="") # D-17
    ativo = models.BooleanField(default=True) # RF-07 (Inativar unidade)

    def __str__(self): #Retorna o nome da instituição para não mostrar "instituição object (1)" no admin.
        return self.nome
class Acolhido(models.Model):
    nome = models.CharField(max_length=100) # D-01 (Nome do acolhido)
    documentacao = models.CharField(max_length=50, blank=True, default="") # D-02 + RN-15 (Documentação do acolhido, ex: RG, CPF)
    justificativa_sem_doc = models.TextField(blank=True, default="") # RN-15 (Justificativa para ausência de documentação)
    data_nascimento = models.DateField() # D-03 (Data de nascimento do acolhido)
    genero = models.CharField(max_length=20) # D-04 (Gênero do acolhido)
    familiares = models.TextField(blank=True, default="") # D-05 (Informações sobre familiares do acolhido para possível contato)
    nome_pais = models.CharField(max_length=150, blank=True, default="") # D-06 (Nome dos pais do acolhido, se conhecido)
    endereco = models.CharField(max_length=200, blank=True, default="") # D-07 (Endereço completo do acolhido, se conhecido)
    renda = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True) # D-08 (Renda mensal do acolhido, se houver)
    historico_saude = models.TextField(blank=True, default="") # D-09 (Informações sobre histórico de saúde do acolhido)
    orientacao_sexual = models.CharField(max_length=30, blank=True, default="") # D-10 (Orientação sexual do acolhido, se conhecido)
    motivo_acolhimento = models.TextField() # D-11 (Motivo do acolhimento do indivíduo)
    ativo = models.BooleanField(default=True) # RF-02 (Inativar acolhido)

    def __str__(self): #Retorna o nome do acolhido para não mostrar "acolhido object (1)" no admin.
        return self.nome
