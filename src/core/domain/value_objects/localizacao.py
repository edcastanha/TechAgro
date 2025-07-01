from dataclasses import dataclass, field
from src.core.domain.exceptions.exceptions import ErroValidacaoLocalizacao

@dataclass(frozen=True)
class Localizacao:
    """
    Objeto de Valor para representar a localização geográfica.
    """
    cidade: str = field(metadata={'description': 'O nome da cidade.'})
    estado: str = field(metadata={'description': 'A sigla do estado (UF).'}) # Ex: "CE", "SP"

    def __post_init__(self):
        """
        Método chamado após a inicialização para validação.
        """
        if not self.cidade or not self.cidade.strip():
            raise ErroValidacaoLocalizacao("A cidade não pode estar vazia.")
        
        # Converte a sigla do estado para maiúsculas
        object.__setattr__(self, 'estado', self.estado.upper().strip())

        if not self.estado or len(self.estado) != 2:
            raise ErroValidacaoLocalizacao("O estado deve ser uma sigla de 2 letras (UF).")
        
        # TODO: Implementar validação para checar se a UF é válida (ex: consultar uma lista)
        # if self.estado not in LISTA_DE_UFS_VALIDAS:
        #     raise ErroValidacaoLocalizacao(f"UF '{self.estado}' inválida.")

    def __str__(self):
        """
        Retorna a representação em string da localização.
        """
        return f"{self.cidade}, {self.estado}"