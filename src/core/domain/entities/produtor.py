import uuid
from dataclasses import dataclass, field
from typing import Union, List, Optional
from src.core.domain.entities.responsavel_legal import Pessoa, Empresa
from src.core.domain.exceptions.exceptions import ErroValidacaoProdutor

@dataclass(eq=False)
class Produtor:
    """
    Entidade Produtor Rural. Representa o papel de um produtor,
    que pode ser uma Pessoa Física ou uma Pessoa Jurídica (Empresa).
    É a raiz de um Agregado.
    """
    id: str = field(default_factory=lambda: str(uuid.uuid4()), init=False,
                    metadata={'description': 'Identificador único do Produtor.'})
    # O Produtor pode ser uma Pessoa ou uma Empresa, mas não ambos.
    pessoa: Optional[Pessoa] = field(default=None,
                                     metadata={'description': 'Pessoa Física associada ao produtor.'})
    empresa: Optional[Empresa] = field(default=None,
                                      metadata={'description': 'Empresa associada ao produtor.'})

    def __post_init__(self):
        """
        Validações pós-inicialização para a entidade Produtor.
        Garanta que o produtor seja Pessoa OU Empresa, mas não ambos.
        """
        # XOR lógico (um DEVE ser True, o outro DEVE ser False)
        if not ((self.pessoa is not None) ^ (self.empresa is not None)):
            raise ErroValidacaoProdutor("O produtor deve ser associado a uma Pessoa ou a uma Empresa, mas não a ambos.")

    @property
    def nome(self) -> str:
        """
        Retorna o nome ou razão social do produtor.
        """
        if self.pessoa:
            return self.pessoa.nome
        elif self.empresa:
            return self.empresa.razao_social
        return "Nome Indefinido" # Caso o post_init falhe por algum motivo, embora não devesse.

    @property
    def documento(self) -> Union[str, None]:
        """
        Retorna o CPF ou CNPJ do produtor.
        """
        if self.pessoa and self.pessoa.cpf:
            return self.pessoa.cpf.valor
        elif self.empresa and self.empresa.cnpj:
            return self.empresa.cnpj.valor
        return None

    def __eq__(self, other):
        """
        Define a igualdade entre dois Produtores pela sua ID.
        """
        if not isinstance(other, Produtor):
            return NotImplemented
        return self.id == other.id

    def __hash__(self):
        """
        Define o hash do Produtor baseado na sua ID.
        """
        return hash(self.id)