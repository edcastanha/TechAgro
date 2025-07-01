# src/application/dtos/atividade_rural_dtos.py (AJUSTADO)

from dataclasses import dataclass
from typing import Optional

# DTOs de entrada para Atividade Rural

@dataclass
class CriarAtividadeRuralInputDTO:
    """DTO de entrada para o caso de uso de criação de Atividade Rural."""
    safra_id: str
    nome_atividade: str
    ramo: str # O ramo da atividade como string (ex: "AGRICULTURA", "PECUARIA") - será convertido para Enum no caso de uso
    area_afetada_ha: Optional[float] = None

@dataclass
class AtualizarAtividadeRuralInputDTO:
    """DTO de entrada para o caso de uso de atualização de Atividade Rural."""
    atividade_id: str
    nome_atividade: Optional[str] = None
    ramo: Optional[str] = None # O ramo da atividade como string
    area_afetada_ha: Optional[float] = None

# DTOs de saída para Atividade Rural

@dataclass
class AtividadeRuralOutputDTO:
    """DTO de saída para representar uma Atividade Rural."""
    id: str
    safra_id: str
    nome_atividade: str
    ramo: str # Retorna o nome do ramo como string para o cliente
    area_afetada_ha: Optional[float] = None