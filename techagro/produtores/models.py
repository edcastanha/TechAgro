import re
import uuid
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError

def validate_cpf(value):
    """
    Valida um CPF. Exemplo simplificado, para uma validação robusta,
    considere bibliotecas como 'django-cpf-cnpj'.
    """
    cpf = re.sub(r'[^0-9]', '', value)
    if len(cpf) != 11:
        raise ValidationError({'documento': 'CPF deve ter 11 dígitos.'})
    if cpf == cpf[0] * 11:
        raise ValidationError({'documento': 'CPF inválido (todos os dígitos iguais).'})
    # Validação dos dígitos verificadores (simplificada)
    for i in range(9, 11):
        soma = sum(int(cpf[num]) * ((i+1) - num) for num in range(0, i))
        digito = ((soma * 10) % 11) % 10
        if digito != int(cpf[i]):
            raise ValidationError({'documento': 'CPF inválido.'})
    return value

def validate_cnpj(value):
    """
    Valida um CNPJ. Exemplo simplificado.
    """
    cnpj = re.sub(r'[^0-9]', '', value)
    if len(cnpj) != 14:
        raise ValidationError({'documento': 'CNPJ deve ter 14 dígitos.'})
    if cnpj == cnpj[0] * 14:
        raise ValidationError({'documento': 'CNPJ inválido (todos os dígitos iguais).'})
    # Validação dos dígitos verificadores (simplificada)
    pesos1 = [5,4,3,2,9,8,7,6,5,4,3,2]
    pesos2 = [6] + pesos1
    for i, pesos in enumerate([pesos1, pesos2]):
        soma = sum(int(cnpj[num]) * pesos[num] for num in range(len(pesos)))
        digito = 11 - soma % 11
        if digito >= 10:
            digito = 0
        if digito != int(cnpj[12 + i]):
            raise ValidationError({'documento': 'CNPJ inválido.'})
    return value

def validate_areas_propriedade(area_total, area_agricultavel, area_vegetacao):
    if (area_agricultavel is not None and area_vegetacao is not None and area_total is not None):
        if (area_agricultavel + area_vegetacao) > area_total:
            raise ValidationError({
                'area_agricultavel_hectares': 'A soma da área agricultável e de vegetação não pode exceder a área total da Propriedade.',
                'area_vegetacao_hectares': 'A soma da área agricultável e de vegetação não pode exceder a área total da Propriedade.'
            })

class BaseModel(models.Model):
    """
    Classe base para modelos, pode ser usada para adicionar campos comuns no futuro.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, help_text="Data e hora de criação do registro.")
    updated_at = models.DateTimeField(auto_now=True, help_text="Data e hora da última atualização do registro.")
    class Meta:
        abstract = True

class Endereco(models.Model):
    """
    Modelo abstrato para representar um endereço detalhado.
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
        validators=[MinValueValidator(-90), MaxValueValidator(90)],
        help_text="Latitude da propriedade (ex: -23.55052)."
    )
    longitude = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True,
        validators=[MinValueValidator(-180), MaxValueValidator(180)],
        help_text="Longitude da propriedade (ex: -46.63330)."
    )
    class Meta:
        abstract = True

class Produtor(BaseModel):
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
    nome = models.CharField(
        max_length=255,
        help_text="Nome completo do produtor ou razão social da empresa."
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
        """
        Sobrescreve o método save para garantir que clean() seja chamado.
        Em formulários e admin, clean() é chamado automaticamente.
        Para saves diretos (ex: shell), é bom garantir.
        """
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nome

class Propriedade(Endereco, BaseModel):
    """
    Modelo para representar uma Propriedade (Propriedade Rural) pertencente a um produtor,
    agora com endereço detalhado e tipo de atividade.
    """
    TIPO_ATIVIDADE_CHOICES = [
        ('AGRICULTURA', 'Agricultura'),
        ('PECUARIA', 'Pecuária'),
        ('AGROPECUARIA', 'Agropecuária'),
        ('OUTRO', 'Outro'),
    ]

    produtor = models.ForeignKey(
        Produtor,
        on_delete=models.CASCADE,
        related_name='propriedades',
        help_text="Produtor rural responsável por esta Propriedade."
    )
    nome_propriedade = models.CharField(
        max_length=255,
        help_text="Nome da Propriedade ou propriedade rural."
    )
    tipo_atividade = models.CharField(
        max_length=20,
        choices=TIPO_ATIVIDADE_CHOICES,
        default='AGROPECUARIA',
        help_text="Principal tipo de atividade da Propriedade."
    )
    area_total_hectares = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
        help_text="Área total da Propriedade em hectares."
    )
    area_agricultavel_hectares = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        help_text="Área em hectares que pode ser usada para plantio."
    )
    area_vegetacao_hectares = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        help_text="Área em hectares com vegetação nativa ou preservação."
    )

    class Meta:
        verbose_name = "Propriedade"
        verbose_name_plural = "Propriedades"
        unique_together = ('produtor', 'nome_propriedade')
        ordering = ['nome_propriedade']

    def clean(self):
        validate_areas_propriedade(
            self.area_total_hectares,
            self.area_agricultavel_hectares,
            self.area_vegetacao_hectares
        )

    def __str__(self):
        return f"{self.nome_propriedade} ({self.cidade}/{self.estado}) - Produtor: {self.produtor.nome}"

class Safra(BaseModel):
    """
    Modelo para representar uma Safra agrícola associada a uma Propriedade,
    com período de início e fim.
    """
    propriedade = models.ForeignKey(
        Propriedade,
        on_delete=models.CASCADE,
        related_name='safras',
        help_text="Propriedade onde esta safra foi cultivada."
    )
    ano = models.IntegerField(
        help_text="Ano da safra (ex: 2023)."
    )
    data_inicio = models.DateField(
        null=True,
        blank=True,
        help_text="Data de início da safra (dia/mês/ano)."
    )
    data_fim = models.DateField(
        null=True,
        blank=True,
        help_text="Data de fim da safra (dia/mês/ano)."
    )
    descricao = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Descrição opcional da safra (ex: Safra de Verão)."
    )

    class Meta:
        verbose_name = "Safra"
        verbose_name_plural = "Safras"
        unique_together = ('propriedade', 'ano')
        ordering = ['-ano']

    def clean(self):
        """
        Validação para garantir que a data de fim não seja anterior à data de início,
        e que o ano das datas corresponda ao campo 'ano' da safra.
        """
        if self.data_inicio and self.data_fim:
            if self.data_fim < self.data_inicio:
                raise ValidationError({'data_fim': 'A data de fim não pode ser anterior à data de início.'})

            if self.data_inicio.year != self.ano or self.data_fim.year != self.ano:
                raise ValidationError({
                    'ano': 'O ano das datas de início e fim deve corresponder ao ano da safra.'
                })
        elif self.data_inicio and not self.data_fim:
            raise ValidationError({'data_fim': 'Se a data de início for preenchida, a data de fim também deve ser.'})
        elif not self.data_inicio and self.data_fim:
            raise ValidationError({'data_inicio': 'Se a data de fim for preenchida, a data de início também deve ser.'})


    def __str__(self):
        return f"Safra {self.ano} na {self.propriedade.nome_propriedade}"    
    
class AtividadeRural(BaseModel):
    """
    Modelo para registrar as culturas específicas plantadas em uma Safra.
    """
    safra = models.ForeignKey(
        Safra,
        on_delete=models.CASCADE,
        related_name='culturas_plantadas',
        help_text="Safra à qual esta cultura pertence."
    )
    nome_cultura = models.CharField(
        max_length=100,
        help_text="Nome da cultura plantada (ex: Soja, Milho, Café)."
    )
    area_plantada_hectares = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        blank=True,
        null=True,
        help_text="Área específica em hectares que esta cultura ocupou nesta safra (opcional)."
    )
    data_plantio = models.DateField(
        blank=True,
        null=True,
        help_text="Data em que a cultura foi plantada (opcional)."
    )
    data_colheita = models.DateField(
        blank=True,
        null=True,
        help_text="Data em que a cultura foi colhida (opcional)."
    )

    class Meta:
        verbose_name = "Cultura Plantada"
        verbose_name_plural = "Culturas Plantadas"
        unique_together = ('safra', 'nome_cultura') # Uma safra só pode ter uma entrada para a mesma cultura
        ordering = ['nome_cultura']

    def __str__(self):
        return f"{self.nome_cultura} - {self.safra.ano} ({self.safra.propriedade.nome_propriedade})"
