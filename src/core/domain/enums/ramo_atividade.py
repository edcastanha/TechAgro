# src/core/domain/enums/ramo_atividade.py

from enum import Enum

class RamoAtividade(Enum):
    """
    Enumeração para definir os ramos principais de atividade rural.
    """
    AGRICULTURA = "AGRICULTURA"
    PECUARIA = "PECUARIA"
    SILVICULTURA = "SILVICULTURA"
    AQUICULTURA = "AQUICULTURA"
    OUTROS = "OUTROS"

    def __str__(self):
        """Retorna o valor do enum como string."""
        return self.value

    def __repr__(self):
        """Retorna a representação do enum."""
        return f"<RamoAtividade.{self.name}>"