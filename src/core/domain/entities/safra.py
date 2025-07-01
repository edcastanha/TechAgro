# src/core/domain/entities/safra.py

import uuid
from dataclasses import dataclass, field
from src.core.domain.exceptions.exceptions import ErroValidacaoSafra
from typing import Optional

@dataclass(eq=False)
class Safra:
    """
    Entidade que representa uma Safra agrícola.
    Está associada a uma Propriedade Rural.
    """
    id: str = field(default_factory=lambda: str(uuid.uuid4()), init=False,
                    metadata={'description': 'Identificador único da Safra.'})
    ano: int = field(metadata={'description': 'Ano da safra (ex: 2023).'})
    nome_personalizado: str = field(metadata={'description': 'Nome descritivo da safra (ex: "Safra Verão 2023").'})
    # propriedade_id: str # Referência ao ID da Propriedade Rural (para agregação via repositório)

    def __post_init__(self):
        """
        Validações pós-inicialização para a entidade Safra.
        """
        if self.ano <= 0:
            raise ErroValidacaoSafra("O ano da safra deve ser um valor positivo.")
        if not self.nome_personalizado or not self.nome_personalizado.strip():
            raise ErroValidacaoSafra("O nome personalizado da safra não pode estar vazio.")

    def __eq__(self, other):
        """
        Define a igualdade entre duas Safras pela sua ID.
        """
        if not isinstance(other, Safra):
            return NotImplemented
        return self.id == other.id

    def __hash__(self):
        """
        Define o hash da Safra baseado na sua ID.
        """
        return hash(self.id)