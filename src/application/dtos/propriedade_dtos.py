# src/application/dtos/propriedade_dtos.py (AJUSTADO)

from dataclasses import dataclass
from typing import Optional

# DTOs de entrada para Propriedade Rural

@dataclass
class CriarPropriedadeRuralInputDTO:
    """DTO de entrada para o caso de uso de criação de Propriedade Rural."""
    produtor_id: str # O ID do produtor ao qual a propriedade será associada
    nome_fazenda: str
    
    # Novos campos para o Endereco
    logradouro: str
    numero: str
    complemento: Optional[str] = None
    bairro: str
    cep: str
    cidade: str
    estado: str

    area_total_ha: float
    area_agricultavel_ha: float
    area_vegetacao_ha: float

@dataclass
class AtualizarPropriedadeRuralInputDTO:
    """DTO de entrada para o caso de uso de atualização de Propriedade Rural."""
    propriedade_id: str
    nome_fazenda: Optional[str] = None
    
    # Campos opcionais para atualização do Endereco
    logradouro: Optional[str] = None
    numero: Optional[str] = None
    complemento: Optional[str] = None
    bairro: Optional[str] = None
    cep: Optional[str] = None
    cidade: Optional[str] = None
    estado: Optional[str] = None

    area_total_ha: Optional[float] = None
    area_agricultavel_ha: Optional[float] = None
    area_vegetacao_ha: Optional[float] = None

# DTOs de saída para Propriedade Rural

@dataclass
class PropriedadeRuralOutputDTO:
    """DTO de saída para representar uma Propriedade Rural."""
    id: str
    nome_fazenda: str
    produtor_id: str
    
    # Campos de Endereço no DTO de saída
    logradouro: str
    numero: str
    complemento: Optional[str]
    bairro: Optional[str]
    cep: str
    cidade: str
    estado: str

    area_total_ha: float
    area_agricultavel_ha: float
    area_vegetacao_ha: float
    area_nao_utilizada_ha: float # Calculada