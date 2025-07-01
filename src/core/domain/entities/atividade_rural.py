# src/core/domain/entities/atividade_rural.py (AJUSTADO)

import uuid
from dataclasses import dataclass, field
from src.core.domain.exceptions.exceptions import ErroValidacaoAtividadeRural
from src.core.domain.value_objects.areas import MedidaArea
from src.core.domain.enums.ramo_atividade import RamoAtividade
from typing import Optional

@dataclass(eq=False)
class AtividadeRural:
    """
    Entidade que representa uma Atividade Rural dentro de uma safra.
    Pode ser um cultivo (soja, milho) ou outra atividade (pecuária, silvicultura).
    """
    id: str = field(default_factory=lambda: str(uuid.uuid4()), init=False,
                    metadata={'description': 'Identificador único da Atividade Rural.'})
    nome_atividade: str = field(metadata={'description': 'Nome descritivo da atividade (ex: "Plantio de Soja", "Criação de Gado Nelore").'})
    ramo: RamoAtividade = field(metadata={'description': 'Ramo de atividade ao qual esta atividade pertence (Agricultura, Pecuária, etc.).'}) # NOVO ATRIBUTO
    # safra_id: str # Referência ao ID da Safra à qual esta atividade pertence
    area_afetada: Optional[MedidaArea] = field(default=None,
                                            metadata={'description': 'Área específica da propriedade afetada por esta atividade (opcional).'})
    # Você pode adicionar outros atributos aqui que caracterizem uma atividade rural,
    # como data de início/fim, insumos utilizados, etc.

    def __post_init__(self):
        """
        Validações pós-inicialização para a entidade AtividadeRural.
        """
        if not self.nome_atividade or not self.nome_atividade.strip():
            raise ErroValidacaoAtividadeRural("O nome da atividade rural não pode estar vazio.")
        
        # Garante que o ramo seja uma instância do Enum RamoAtividade
        if not isinstance(self.ramo, RamoAtividade):
            raise ErroValidacaoAtividadeRural("O ramo da atividade deve ser um valor válido de RamoAtividade (Enum).")
        
        # Se uma área afetada for fornecida, garanta que não seja negativa (já validado no VO MedidaArea, mas bom ter um sanity check)
        if self.area_afetada and self.area_afetada.valor_em_hectares < 0:
             raise ErroValidacaoAtividadeRural("A área afetada não pode ser negativa.")

    def __eq__(self, other):
        """
        Define a igualdade entre duas Atividades Rurais pela sua ID.
        """
        if not isinstance(other, AtividadeRural):
            return NotImplemented
        return self.id == other.id

    def __hash__(self):
        """
        Define o hash da Atividade Rural baseado na sua ID.
        """
        return hash(self.id)