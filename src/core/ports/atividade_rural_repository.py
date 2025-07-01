# src/core/ports/atividade_rural_repository.py

from abc import ABC, abstractmethod
from typing import Optional, List
from src.core.domain.entities.atividade_rural import AtividadeRural

class IAtividadeRuralRepository(ABC):
    """
    Interface (Port) para o Repositório de Atividades Rurais.
    Define os métodos para manipulação de atividades rurais.
    """

    @abstractmethod
    def salvar(self, atividade: AtividadeRural, safra_id: str) -> None:
        """
        Salva uma nova atividade rural ou atualiza uma existente.
        Associa a atividade a uma safra existente através do ID da safra.
        """
        pass

    @abstractmethod
    def buscar_por_id(self, atividade_id: str) -> Optional[AtividadeRural]:
        """
        Busca uma atividade rural pelo seu ID. Retorna None se não encontrada.
        """
        pass

    @abstractmethod
    def buscar_todas_por_safra(self, safra_id: str) -> List[AtividadeRural]:
        """
        Busca todas as atividades rurais para uma dada safra.
        """
        pass

    @abstractmethod
    def deletar(self, atividade_id: str) -> None:
        """
        Deleta uma atividade rural pelo seu ID.
        """
        pass