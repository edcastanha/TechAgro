# src/core/domain/entities/pessoa_ou_empresa.py (AJUSTADO)

import uuid
from dataclasses import dataclass, field
from src.core.domain.value_objects.documentos import CPF, CNPJ
from src.core.domain.entities.responsavel_legal import ResponsavelLegal

@dataclass(eq=False)
class Pessoa(ResponsavelLegal): # Herda de ResponsavelLegal
    """
    Entidade que representa uma Pessoa Física.
    Também pode atuar como Responsável Legal.
    """
    id: str = field(default_factory=lambda: str(uuid.uuid4()), init=False,
                    metadata={'description': 'Identificador único da Pessoa.'})
    nome: str = field(metadata={'description': 'Nome completo da pessoa.'})
    cpf: CPF = field(metadata={'description': 'Objeto de valor CPF da pessoa.'})

    def __post_init__(self):
        if not self.nome or not self.nome.strip():
            raise ValueError("O nome da pessoa não pode ser vazio.")

    def obter_nome_completo_ou_razao_social(self) -> str:
        return self.nome

    def obter_documento_principal(self) -> CPF:
        return self.cpf
    
    def eh_pessoa_fisica(self) -> bool:
        return True

    def eh_pessoa_juridica(self) -> bool:
        return False

    def __eq__(self, other):
        if not isinstance(other, Pessoa):
            return NotImplemented
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)

@dataclass(eq=False)
class Empresa(ResponsavelLegal): # Herda de ResponsavelLegal
    """
    Entidade que representa uma Pessoa Jurídica (Empresa).
    Também pode atuar como Responsável Legal.
    """
    id: str = field(default_factory=lambda: str(uuid.uuid4()), init=False,
                    metadata={'description': 'Identificador único da Empresa.'})
    razao_social: str = field(metadata={'description': 'Razão social da empresa.'})
    cnpj: CNPJ = field(metadata={'description': 'Objeto de valor CNPJ da empresa.'})
    nome_fantasia: str | None = field(default=None,
                                    metadata={'description': 'Nome fantasia da empresa (opcional).'})

    def __post_init__(self):
        if not self.razao_social or not self.razao_social.strip():
            raise ValueError("A razão social da empresa não pode ser vazia.")

    def obter_nome_completo_ou_razao_social(self) -> str:
        return self.razao_social

    def obter_documento_principal(self) -> CNPJ:
        return self.cnpj
    
    def eh_pessoa_fisica(self) -> bool:
        return False

    def eh_pessoa_juridica(self) -> bool:
        return True

    def __eq__(self, other):
        if not isinstance(other, Empresa):
            return NotImplemented
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)