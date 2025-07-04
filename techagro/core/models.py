import uuid
import re
from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser
from .base import BaseModel
from .validators import validate_cpf, validate_cnpj

class Pessoa(BaseModel):
    """
    Modelo base abstrato para conter informações pessoais comuns
    a todos os tipos de usuários e contatos no sistema.
    """
    nome = models.CharField(max_length=255, help_text="Nome completo ou Razão Social.")
    email = models.EmailField(unique=True, max_length=255, help_text="Endereço de e-mail.")
    telefone = models.CharField(max_length=20, blank=True, null=True, help_text="Número de telefone para contato.")
    
    class Meta:
        abstract = True
        ordering = ['nome']

    def __str__(self):
        return self.nome

class Endereco(BaseModel):
    """
    Modelo para representar um endereço detalhado.
    """
    cep = models.CharField(
        max_length=9, blank=True, null=True,
        help_text="CEP da propriedade (opcional)."
    )
    logradouro = models.CharField(
        max_length=255, blank=True, null=True,
        help_text="Rua, avenida, estrada etc. (opcional)."
    )
    numero = models.CharField(
        max_length=10, blank=True, null=True,
        help_text="Número do imóvel (opcional)."
    )
    complemento = models.CharField(
        max_length=100, blank=True, null=True,
        help_text="Complemento do endereço (ex: Lote 12, Fundos) (opcional)."
    )
    bairro = models.CharField(
        max_length=100, blank=True, null=True,
        help_text="Bairro onde a Propriedade está localizada (opcional)."
    )
    cidade = models.CharField(
        max_length=100,
        help_text="Cidade onde a Propriedade está localizada."
    )
    estado = models.CharField(
        max_length=2,
        help_text="Sigla do estado (UF) onde a Propriedade está localizada."
    )
    latitude = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True,
        help_text="Latitude da propriedade (ex: -23.55052)."
    )
    longitude = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True,
        help_text="Longitude da propriedade (ex: -46.63330)."
    )
    class Meta:
        verbose_name = "Endereço"
        verbose_name_plural = "Endereços"

class User(AbstractUser, BaseModel):
    """
    Modelo de usuário customizado. Por enquanto, usa o padrão do Django,
    mas está pronto para futuras customizações.
    """
    
    def __str__(self):
        return self.username

class ProdutorRural(Pessoa):
    """
    Modelo para representar um Produtor Rural. Pode ser uma pessoa física (CPF)
    ou jurídica (CNPJ). O tipo de documento é inferido e validado.
    """
    TIPO_DOCUMENTO_CHOICES = [
        ('CPF', 'CPF'),
        ('CNPJ', 'CNPJ'),
    ]

    documento = models.CharField(
        max_length=18, # Suficiente para CPF e CNPJ com máscaras (e.g., 999.999.999-99)
        unique=True,
        help_text="CPF (11 dígitos) ou CNPJ (14 dígitos). Somente números, ou com máscara."
    )
    tipo_documento = models.CharField(
        max_length=4,
        choices=TIPO_DOCUMENTO_CHOICES,
        help_text="Tipo de documento (CPF ou CNPJ), inferido automaticamente."
    )

    class Meta:
        verbose_name = "Produtor Rural"
        verbose_name_plural = "Produtores Rurais"
        ordering = ['nome']

    def clean(self):
        """
        Valida o documento e infere o tipo (CPF/CNPJ) baseado no número de dígitos.
        """
        cleaned_document = re.sub(r'[^0-9]', '', self.documento) # Remove caracteres não numéricos

        if len(cleaned_document) == 11:
            self.tipo_documento = 'CPF'
            validate_cpf(cleaned_document)
        elif len(cleaned_document) == 14:
            self.tipo_documento = 'CNPJ'
            validate_cnpj(cleaned_document)
        else:
            raise ValidationError({
                'documento': 'Documento deve ter 11 dígitos (CPF) ou 14 dígitos (CNPJ).'
            })

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

class TecnicoAgricola(Pessoa):
    """
    Modelo para representar um Técnico Agrícola (Agente de Campo).
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='tecnico_agricola',
        help_text="Usuário associado a este Técnico Agrícola."
    )
    registro_profissional = models.CharField(
        max_length=50, unique=True, blank=True, null=True,
        help_text="Número de registro profissional do técnico (ex: CREA, CRMV)."
    )

    class Meta:
        verbose_name = "Técnico Agrícola"
        verbose_name_plural = "Técnicos Agrícolas"
        ordering = ['nome']

class AgenteEscritorio(Pessoa):
    """
    Modelo para representar um Agente de Escritório.
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='agente_escritorio',
        help_text="Usuário associado a este Agente de Escritório."
    )
    departamento = models.CharField(
        max_length=100, blank=True, null=True,
        help_text="Departamento do agente de escritório."
    )

    class Meta:
        verbose_name = "Agente de Escritório"
        verbose_name_plural = "Agentes de Escritório"
        ordering = ['nome']


# Futuramente, outros modelos como Tecnico, AgenteEscritorio, etc.
# herdarão ou se relacionarão com um modelo de usuário que usa estes campos.