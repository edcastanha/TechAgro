# src/core/ports/produtor_repository.py

from abc import ABC, abstractmethod
from typing import Optional, List
from src.core.domain.entities.produtor import Produtor
from src.core.domain.entities.propriedade_rural import PropriedadeRural # Se quiser carregar propriedades junto

class IProdutorRepository(ABC):
    """
    Interface (Port) para o Repositório de Produtores Rurais.
    Define os métodos que qualquer implementação concreta de repositório de produtor deve ter.
    """

    @abstractmethod
    def salvar(self, produtor: Produtor) -> None:
        """
        Salva um novo produtor ou atualiza um existente no repositório.
        """
        pass

    @abstractmethod
    def buscar_por_id(self, produtor_id: str) -> Optional[Produtor]:
        """
        Busca um produtor pelo seu ID. Retorna None se não encontrado.
        """
        pass

    @abstractmethod
    def buscar_todos(self) -> List[Produtor]:
        """
        Busca todos os produtores registrados.
        """
        pass

    @abstractmethod
    def buscar_por_documento(self, documento: str) -> Optional[Produtor]:
        """
        Busca um produtor pelo CPF ou CNPJ. Retorna None se não encontrado.
        """
        pass

    @abstractmethod
    def deletar(self, produtor_id: str) -> None:
        """
        Deleta um produtor pelo seu ID.
        """
        pass

    # Exemplo de método para carregar agregados (propriedades de um produtor)
    @abstractmethod
    def buscar_propriedades_do_produtor(self, produtor_id: str) -> List[PropriedadeRural]:
        """
        Busca todas as propriedades rurais associadas a um produtor.
        """
        pass