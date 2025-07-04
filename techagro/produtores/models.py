import re
import uuid
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from core.validators import validate_areas_propriedade
from core.models import ProdutorRural, Endereco
from core.base import BaseModel

class Propriedade(BaseModel):
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
        ProdutorRural,
        on_delete=models.CASCADE,
        related_name='propriedades',
        help_text="Produtor rural responsável por esta Propriedade."
    )
    endereco = models.OneToOneField(
        Endereco,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        help_text="Endereço da propriedade."
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

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nome_propriedade} ({self.endereco.cidade}/{self.endereco.estado}) - Produtor: {self.produtor.nome}"

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
