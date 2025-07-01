# src/application/dtos/safra_dtos.py

from dataclasses import dataclass
from typing import Optional

# DTOs de entrada para Safra

@dataclass
class CriarSafraInputDTO:
    """DTO de entrada para o caso de uso de criação de Safra."""
    propriedade_id: str # O ID da propriedade à qual a safra será associada
    ano: int
    nome_personalizado: str

@dataclass
class AtualizarSafraInputDTO:
    """DTO de entrada para o caso de uso de atualização de Safra."""
    safra_id: str
    ano: Optional[int] = None
    nome_personalizado: Optional[str] = None

# DTOs de saída para Safra

@dataclass
class SafraOutputDTO:
    """DTO de saída para representar uma Safra."""
    id: str
    propriedade_id: str
    ano: int
    nome_personalizado: str