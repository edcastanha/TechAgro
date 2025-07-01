# src/infrastructure/django_app/models.py

from django.db import models
from django.core.validators import MinValueValidator
import uuid

# --- Modelos Django para Mapeamento de Entidades de Domínio ---

class ResponsavelLegalModel(models.Model):
    """
    Modelo base abstrato para Pessoa Física ou Jurídica.
    Representa a hierarquia ResponsavelLegal do domínio.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # Não tem campos específicos aqui, pois serão nas subclasses.
    # Serve como um 'pointer' para o tipo concreto.

    class Meta:
        abstract = True # Esta é uma classe abstrata e não será criada como tabela no DB

class PessoaModel(ResponsavelLegalModel):
    """
    Modelo Django para mapear a entidade de domínio Pessoa (Física).
    """
    nome = models.CharField(max_length=255)
    cpf = models.CharField(max_length=11, unique=True, db_index=True) # Validar formato no domínio

    class Meta:
        db_table = 'produtor_pessoa' # Nome da tabela no banco de dados

    def __str__(self):
        return self.nome

class EmpresaModel(ResponsavelLegalModel):
    """
    Modelo Django para mapear a entidade de domínio Empresa (Jurídica).
    """
    razao_social = models.CharField(max_length=255)
    cnpj = models.CharField(max_length=14, unique=True, db_index=True) # Validar formato no domínio
    nome_fantasia = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'produtor_empresa' # Nome da tabela no banco de dados

    def __str__(self):
        return self.razao_social

class ProdutorModel(models.Model):
    """
    Modelo Django para mapear a entidade de domínio Produtor Rural.
    Relaciona-se polimorficamente com PessoaModel ou EmpresaModel.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # FK para Pessoa (se for pessoa física) - null=True porque é opcional
    pessoa = models.OneToOneField(PessoaModel, on_delete=models.CASCADE, null=True, blank=True, related_name='produtor')
    # FK para Empresa (se for pessoa jurídica) - null=True porque é opcional
    empresa = models.OneToOneField(EmpresaModel, on_delete=models.CASCADE, null=True, blank=True, related_name='produtor')

    ativo = models.BooleanField(default=True, db_index=True)

    class Meta:
        db_table = 'produtor_rural' # Nome da tabela no banco de dados
        # Adicionar uma restrição para garantir que apenas um dos campos (pessoa ou empresa) seja preenchido
        constraints = [
            models.CheckConstraint(
                check=models.Q(pessoa__isnull=False, empresa__isnull=True) |
                      models.Q(pessoa__isnull=True, empresa__isnull=False),
                name='apenas_um_tipo_de_responsavel'
            )
        ]

    def __str__(self):
        if self.pessoa:
            return self.pessoa.nome
        elif self.empresa:
            return self.empresa.razao_social
        return "Produtor Desconhecido"


class EnderecoModel(models.Model):
    """
    Modelo Django para mapear o Objeto de Valor Endereco.
    Não é uma entidade raiz no DDD, mas precisa de sua própria tabela no DB.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) # Para referenciar se Endereco fosse um Agregado Raiz ou entidade
    logradouro = models.CharField(max_length=255)
    numero = models.CharField(max_length=50) # Pode ser 'S/N'
    complemento = models.CharField(max_length=255, blank=True, null=True)
    bairro = models.CharField(max_length=255)
    cep = models.CharField(max_length=8) # Armazenar apenas dígitos
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=2) # UF, ex: 'SP', 'MG'

    class Meta:
        db_table = 'endereco'

    def __str__(self):
        return f"{self.logradouro}, {self.numero}, {self.cidade}/{self.estado}"


class PropriedadeRuralModel(models.Model):
    """
    Modelo Django para mapear a entidade de domínio PropriedadeRural.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    produtor = models.ForeignKey(ProdutorModel, on_delete=models.CASCADE, related_name='propriedades') # FK para o Produtor
    nome_fazenda = models.CharField(max_length=255)
    
    # Endereço é uma composição (um para um) com PropriedadeRural
    endereco = models.OneToOneField(EnderecoModel, on_delete=models.CASCADE, related_name='propriedade')

    area_total_ha = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    area_agricultavel_ha = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    area_vegetacao_ha = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])

    class Meta:
        db_table = 'propriedade_rural'

    def __str__(self):
        return self.nome_fazenda

# Enum RamoAtividade para o campo de escolha no modelo
# Django não tem um tipo Enum nativo, então usamos Choices ou CharField com validação
# Para simplicidade, vamos usar CharField e mapear para o Enum Python no repositório
RAMO_ATIVIDADE_CHOICES = [
    ("AGRICULTURA", "Agricultura"),
    ("PECUARIA", "Pecuária"),
    ("SILVICULTURA", "Silvicultura"),
    ("AQUICULTURA", "Aquicultura"),
    ("OUTROS", "Outros"),
]

class SafraModel(models.Model):
    """
    Modelo Django para mapear a entidade de domínio Safra.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    propriedade = models.ForeignKey(PropriedadeRuralModel, on_delete=models.CASCADE, related_name='safras')
    ano = models.IntegerField()
    nome_personalizado = models.CharField(max_length=255)

    class Meta:
        db_table = 'safra'
        # Garante que não haja duas safras com o mesmo ano e nome_personalizado para a mesma propriedade
        unique_together = ('propriedade', 'ano', 'nome_personalizado') 

    def __str__(self):
        return f"{self.nome_personalizado} ({self.ano}) - {self.propriedade.nome_fazenda}"

class AtividadeRuralModel(models.Model):
    """
    Modelo Django para mapear a entidade de domínio AtividadeRural.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    safra = models.ForeignKey(SafraModel, on_delete=models.CASCADE, related_name='atividades')
    nome_atividade = models.CharField(max_length=255)
    ramo = models.CharField(max_length=50, choices=RAMO_ATIVIDADE_CHOICES) # Mapeia o Enum RamoAtividade
    area_afetada_ha = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, validators=[MinValueValidator(0)])

    class Meta:
        db_table = 'atividade_rural'

    def __str__(self):
        return self.nome_atividade