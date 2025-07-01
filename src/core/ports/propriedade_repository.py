# src/core/ports/propriedade_repository.py

from abc import ABC, abstractmethod
from typing import Optional, List
from src.core.domain.entities.propriedade_rural import PropriedadeRural
from src.core.domain.entities.safra import Safra # Se quiser carregar safras junto

class IPropriedadeRuralRepository(ABC):
    """
    Interface (Port) para o Repositório de Propriedades Rurais.
    Define os métodos para manipulação de propriedades rurais.
    """

    @abstractmethod
    def salvar(self, propriedade: PropriedadeRural, produtor_id: str) -> None:
        """
        Salva uma nova propriedade ou atualiza uma existente.
        Associa a propriedade a um produtor existente.
        """
        pass

    @abstractmethod
    def buscar_por_id(self, propriedade_id: str) -> Optional[PropriedadeRural]:
        """
        Busca uma propriedade rural pelo seu ID. Retorna None se não encontrada.
        """
        pass

    @abstractmethod
    def buscar_todas(self) -> List[PropriedadeRural]:
        """
        Busca todas as propriedades rurais.
        """
        pass

    @abstractmethod
    def deletar(self, propriedade_id: str) -> None:
        """
        Deleta uma propriedade rural pelo seu ID.
        """
        pass

    @abstractmethod
    def buscar_safras_da_propriedade(self, propriedade_id: str) -> List[Safra]:
        """
        Busca todas as safras associadas a uma propriedade rural.
        """
        pass