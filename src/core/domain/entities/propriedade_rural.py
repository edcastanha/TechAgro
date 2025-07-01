# src/core/domain/entities/propriedade_rural.py (AJUSTADO)

import uuid
from dataclasses import dataclass, field
from src.core.domain.value_objects.areas import MedidaArea
from src.core.domain.value_objects.endereco import Endereco # Importe o NOVO VO Endereco
from src.core.domain.exceptions.exceptions import ErroValidacaoPropriedadeRural
from typing import Optional

@dataclass(eq=False)
class PropriedadeRural:
    """
    Entidade que representa uma Propriedade Rural.
    Pode ser a raiz de um Agregado com Safras e Atividades Rurais.
    """
    id: str = field(default_factory=lambda: str(uuid.uuid4()), init=False,
                    metadata={'description': 'Identificador único da Propriedade Rural.'})
    nome_fazenda: str = field(metadata={'description': 'Nome da fazenda ou propriedade.'})
    endereco: Endereco = field(metadata={'description': 'Objeto de valor de Endereço completo da propriedade.'}) # Agora usa Endereco
    area_total: MedidaArea = field(metadata={'description': 'Área total da propriedade em hectares.'})
    area_agricultavel: MedidaArea = field(metadata={'description': 'Área agricultável da propriedade em hectares.'})
    area_vegetacao: MedidaArea = field(metadata={'description': 'Área de vegetação da propriedade em hectares.'})
    # produtor_id: str # Para ligar a Propriedade a um Produtor (referência por ID, evitando ciclo de importação)

    def __post_init__(self):
        """
        Validações de consistência para a entidade PropriedadeRural.
        """
        if not self.nome_fazenda or not self.nome_fazenda.strip():
            raise ErroValidacaoPropriedadeRural("O nome da fazenda não pode ser vazio.")
        
        if self.area_total.valor_em_hectares <= 0:
            raise ErroValidacaoPropriedadeRural("A área total deve ser um valor positivo.")
            
        # A soma da área agricultável e de vegetação não pode exceder a área total.
        if (self.area_agricultavel.valor_em_hectares + self.area_vegetacao.valor_em_hectares) > self.area_total.valor_em_hectares:
            raise ErroValidacaoPropriedadeRural("A soma da área agricultável e de vegetação não pode exceder a área total da propriedade.")
            
        if self.area_agricultavel.valor_em_hectares < 0 or self.area_vegetacao.valor_em_hectares < 0:
            raise ErroValidacaoPropriedadeRural("As áreas agricultável e de vegetação não podem ser negativas.")

    def calcular_area_nao_utilizada(self) -> MedidaArea:
        """
        Calcula a área da propriedade que não é agricultável nem vegetação.
        """
        area_utilizada = self.area_agricultavel.valor_em_hectares + self.area_vegetacao.valor_em_hectares
        return MedidaArea(self.area_total.valor_em_hectares - area_utilizada)

    def __eq__(self, other):
        """
        Define a igualdade entre duas Propriedades Rurais pela sua ID.
        """
        if not isinstance(other, PropriedadeRural):
            return NotImplemented
        return self.id == other.id

    def __hash__(self):
        """
        Define o hash da Propriedade Rural baseado na sua ID.
        """
        return hash(self.id)