from dataclasses import dataclass, field
from src.core.domain.exceptions.exceptions import ErroValidacaoArea

@dataclass(frozen=True)
class MedidaArea:
    """
    Objeto de Valor para representar medidas de área, geralmente em hectares.
    Encapsula o valor e operações relacionadas.
    """
    valor_em_hectares: float = field(metadata={'description': 'A área em hectares.'})

    def __post_init__(self):
        """
        Método chamado após a inicialização para validação.
        """
        if self.valor_em_hectares < 0:
            raise ErroValidacaoArea("A área não pode ser um valor negativo.")
        # Arredonda para duas casas decimais para consistência, se preferir
        object.__setattr__(self, 'valor_em_hectares', round(self.valor_em_hectares, 2))

    def para_acres(self) -> float:
        """Converte a área de hectares para acres."""
        return self.valor_em_hectares * 2.47105

    def para_metros_quadrados(self) -> float:
        """Converte a área de hectares para metros quadrados."""
        return self.valor_em_hectares * 10000

    def __add__(self, other):
        """Define a operação de adição entre objetos MedidaArea."""
        if isinstance(other, MedidaArea):
            return MedidaArea(self.valor_em_hectares + other.valor_em_hectares)
        raise TypeError("Só é possível adicionar objetos do tipo MedidaArea.")

    def __sub__(self, other):
        """Define a operação de subtração entre objetos MedidaArea."""
        if isinstance(other, MedidaArea):
            return MedidaArea(self.valor_em_hectares - other.valor_em_hectares)
        raise TypeError("Só é possível subtrair objetos do tipo MedidaArea.")

    def __str__(self):
        """Retorna a representação em string da área."""
        return f"{self.valor_em_hectares:.2f} ha"