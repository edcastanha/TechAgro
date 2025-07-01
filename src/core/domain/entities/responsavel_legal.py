# src/core/domain/entities/responsavel_legal.py

from abc import ABC, abstractmethod
from src.core.domain.value_objects.documentos import CPF, CNPJ
from typing import Union, Optional

class ResponsavelLegal(ABC):
    """
    Classe abstrata que define a interface comum para qualquer entidade que possa
    assumir o papel de Responsável Legal por um Produtor (Pessoa Física ou Jurídica).
    """
    id: str

    @abstractmethod
    def obter_nome_completo_ou_razao_social(self) -> str:
        """
        Retorna o nome completo (Pessoa) ou a razão social (Empresa) do responsável legal.
        """
        pass

    @abstractmethod
    def obter_documento_principal(self) -> Union[CPF, CNPJ]:
        """
        Retorna o objeto de valor do documento principal (CPF ou CNPJ).
        """
        pass
    
    @abstractmethod
    def eh_pessoa_fisica(self) -> bool:
        """Indica se o responsável legal é uma pessoa física."""
        pass

    @abstractmethod
    def eh_pessoa_juridica(self) -> bool:
        """Indica se o responsável legal é uma pessoa jurídica."""
        pass