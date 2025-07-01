# src/core/domain/entities/pessoa_ou_empresa.py

import uuid
from dataclasses import dataclass, field
from src.core.domain.value_objects.documentos import CPF, CNPJ
# Não precisamos importar ErroDominio aqui se as validações forem delegadas aos VOs

@dataclass(eq=False) # eq=False: a comparação de igualdade será feita pelo 'id' (identidade)
class Pessoa:
    """
    Entidade que representa uma Pessoa Física.
    """
    id: str = field(default_factory=lambda: str(uuid.uuid4()), init=False,
                    metadata={'description': 'Identificador único da Pessoa.'})
    nome: str = field(metadata={'description': 'Nome completo da pessoa.'})
    cpf: CPF = field(metadata={'description': 'Objeto de valor CPF da pessoa.'})

    def __post_init__(self):
        """
        Validações pós-inicialização para a entidade Pessoa.
        """
        if not self.nome or not self.nome.strip():
            raise ValueError("O nome da pessoa não pode ser vazio.")
        # A validação do CPF já é feita no construtor do Value Object CPF

    def __eq__(self, other):
        """
        Define a igualdade entre duas Pessoas pela sua ID.
        """
        if not isinstance(other, Pessoa):
            return NotImplemented
        return self.id == other.id

    def __hash__(self):
        """
        Define o hash da Pessoa baseado na sua ID.
        """
        return hash(self.id)

@dataclass(eq=False)
class Empresa:
    """
    Entidade que representa uma Pessoa Jurídica (Empresa).
    """
    id: str = field(default_factory=lambda: str(uuid.uuid4()), init=False,
                    metadata={'description': 'Identificador único da Empresa.'})
    razao_social: str = field(metadata={'description': 'Razão social da empresa.'})
    cnpj: CNPJ = field(metadata={'description': 'Objeto de valor CNPJ da empresa.'})
    nome_fantasia: str | None = field(default=None,
                                    metadata={'description': 'Nome fantasia da empresa (opcional).'})

    def __post_init__(self):
        """
        Validações pós-inicialização para a entidade Empresa.
        """
        if not self.razao_social or not self.razao_social.strip():
            raise ValueError("A razão social da empresa não pode ser vazia.")
        # A validação do CNPJ já é feita no construtor do Value Object CNPJ

    def __eq__(self, other):
        """
        Define a igualdade entre duas Empresas pela sua ID.
        """
        if not isinstance(other, Empresa):
            return NotImplemented
        return self.id == other.id

    def __hash__(self):
        """
        Define o hash da Empresa baseado na sua ID.
        """
        return hash(self.id)