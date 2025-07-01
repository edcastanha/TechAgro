from dataclasses import dataclass, field
import re
from src.core.domain.exceptions.exceptions import ErroValidacaoDocumento

@dataclass(frozen=True) # frozen=True torna o objeto imutável (característica de Value Object)
class CPF:
    """
    Objeto de Valor para o Cadastro de Pessoas Físicas (CPF).
    Encapsula o valor e a lógica de validação básica.
    """
    valor: str = field(metadata={'description': 'O valor do CPF como string.'})

    def __post_init__(self):
        """
        Método chamado após a inicialização do dataclass para validação.
        """
        # Remove caracteres não numéricos (pontos, traços)
        cpf_limpo = re.sub(r'\D', '', self.valor)
        object.__setattr__(self, 'valor', cpf_limpo) # Atualiza o valor imutável via hack

        # Validação básica de formato: deve ter 11 dígitos numéricos
        if not re.fullmatch(r'\d{11}', self.valor):
            raise ErroValidacaoDocumento("CPF deve conter exatamente 11 dígitos numéricos.")

        # TODO: Implementar lógica de validação real dos dígitos verificadores do CPF
        # if not self._validar_digitos_verificadores(self.valor):
        #     raise ErroValidacaoDocumento("CPF com dígitos verificadores inválidos.")

    def __str__(self):
        """
        Retorna o CPF formatado para exibição.
        """
        # Ex: 123.456.789-00
        return f"{self.valor[:3]}.{self.valor[3:6]}.{self.valor[6:9]}-{self.valor[9:]}"

    def _validar_digitos_verificadores(self, cpf: str) -> bool:
        """
        Método auxiliar para validação complexa de CPF.
        (A ser implementado: calcular e verificar dígitos)
        """
        # Lógica de validação de CPF completa aqui (algoritmo dos dígitos verificadores)
        return True # Placeholder

@dataclass(frozen=True)
class CNPJ:
    """
    Objeto de Valor para o Cadastro Nacional da Pessoa Jurídica (CNPJ).
    Encapsula o valor e a lógica de validação básica.
    """
    valor: str = field(metadata={'description': 'O valor do CNPJ como string.'})

    def __post_init__(self):
        """
        Método chamado após a inicialização do dataclass para validação.
        """
        # Remove caracteres não numéricos (pontos, traços, barras)
        cnpj_limpo = re.sub(r'\D', '', self.valor)
        object.__setattr__(self, 'valor', cnpj_limpo) # Atualiza o valor imutável via hack

        # Validação básica de formato: deve ter 14 dígitos numéricos
        if not re.fullmatch(r'\d{14}', self.valor):
            raise ErroValidacaoDocumento("CNPJ deve conter exatamente 14 dígitos numéricos.")

        # TODO: Implementar lógica de validação real dos dígitos verificadores do CNPJ
        # if not self._validar_digitos_verificadores(self.valor):
        #     raise ErroValidacaoDocumento("CNPJ com dígitos verificadores inválidos.")

    def __str__(self):
        """
        Retorna o CNPJ formatado para exibição.
        """
        # Ex: 00.000.000/0001-00
        return f"{self.valor[:2]}.{self.valor[2:5]}.{self.valor[5:8]}/{self.valor[8:12]}-{self.valor[12:]}"

    def _validar_digitos_verificadores(self, cnpj: str) -> bool:
        """
        Método auxiliar para validação complexa de CNPJ.
        (A ser implementado: calcular e verificar dígitos)
        """
        # Lógica de validação de CNPJ completa aqui
        return True # Placeholder