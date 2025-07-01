# src/application/dtos/atividade_rural_dtos.py

from dataclasses import dataclass
from typing import Optional

# DTOs de entrada para Atividade Rural

@dataclass
class CriarAtividadeRuralInputDTO:
    """DTO de entrada para o caso de uso de criação de Atividade Rural."""
    safra_id: str # O ID da safra à qual a atividade será associada
    nome_atividade: str
    area_afetada_ha: Optional[float] = None # Em hectares

@dataclass
class AtualizarAtividadeRuralInputDTO:
    """DTO de entrada para o caso de uso de atualização de Atividade Rural."""
    atividade_id: str
    nome_atividade: Optional[str] = None
    area_afetada_ha: Optional[float] = None

# DTOs de saída para Atividade Rural

@dataclass
class AtividadeRuralOutputDTO:
    """DTO de saída para representar uma Atividade Rural."""
    id: str
    safra_id: str
    nome_atividade: str
    area_afetada_ha: Optional[float] = None