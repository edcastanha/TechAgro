# src/core/domain/entities/produtor.py (AJUSTADO)

import uuid
from dataclasses import dataclass, field
from typing import Union, List, Optional
from src.core.domain.entities.responsavel_legal import ResponsavelLegal
from src.core.domain.exceptions.exceptions import ErroValidacaoProdutor

@dataclass(eq=False)
class Produtor:
    """
    Entidade Produtor Rural. Representa o papel de um produtor,
    associado a um Responsável Legal (Pessoa Física ou Jurídica).
    É a raiz de um Agregado.
    """
    id: str = field(default_factory=lambda: str(uuid.uuid4()), init=False,
                    metadata={'description': 'Identificador único do Produtor.'})
    # O Produtor é associado a um único ResponsávelLegal (Pessoa ou Empresa)
    responsavel_legal: ResponsavelLegal = field(metadata={'description': 'O responsável legal pelo produtor.'})

    def __post_init__(self):
        """
        Validações pós-inicialização para a entidade Produtor.
        """
        if not self.responsavel_legal:
            raise ErroValidacaoProdutor("O produtor deve ter um responsável legal associado.")

    @property
    def nome(self) -> str:
        """
        Retorna o nome ou razão social do responsável legal do produtor.
        """
        return self.responsavel_legal.obter_nome_completo_ou_razao_social()

    @property
    def documento(self) -> str:
        """
        Retorna o valor do documento principal (CPF ou CNPJ) do responsável legal.
        """
        return self.responsavel_legal.obter_documento_principal().valor # Acessa o valor do VO

    def eh_pessoa_fisica(self) -> bool:
        """Verifica se o produtor é uma pessoa física."""
        return self.responsavel_legal.eh_pessoa_fisica()

    def eh_pessoa_juridica(self) -> bool:
        """Verifica se o produtor é uma pessoa jurídica."""
        return self.responsavel_legal.eh_pessoa_juridica()

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