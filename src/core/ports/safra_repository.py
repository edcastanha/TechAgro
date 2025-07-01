# src/core/ports/safra_repository.py

from abc import ABC, abstractmethod
from typing import Optional, List
from src.core.domain.entities.safra import Safra
from src.core.domain.entities.atividade_rural import AtividadeRural # Se quiser carregar atividades junto

class ISafraRepository(ABC):
    """
    Interface (Port) para o Repositório de Safras.
    Define os métodos para manipulação de safras.
    """

    @abstractmethod
    def salvar(self, safra: Safra, propriedade_id: str) -> None:
        """
        Salva uma nova safra ou atualiza uma existente.
        Associa a safra a uma propriedade rural existente.
        """
        pass

    @abstractmethod
    def buscar_por_id(self, safra_id: str) -> Optional[Safra]:
        """
        Busca uma safra pelo seu ID. Retorna None se não encontrada.
        """
        pass

    @abstractmethod
    def buscar_todas_por_propriedade(self, propriedade_id: str) -> List[Safra]:
        """
        Busca todas as safras para uma dada propriedade rural.
        """
        pass

    @abstractmethod
    def deletar(self, safra_id: str) -> None:
        """
        Deleta uma safra pelo seu ID.
        """
        pass

    @abstractmethod
    def buscar_atividades_da_safra(self, safra_id: str) -> List[AtividadeRural]:
        """
        Busca todas as atividades rurais associadas a uma safra.
        """
        pass