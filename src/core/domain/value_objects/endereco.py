# src/core/domain/value_objects/endereco.py

from dataclasses import dataclass, field
from src.core.domain.value_objects.localizacao import Localizacao
from src.core.domain.exceptions.exceptions import ErroValidacaoLocalizacao # Reutilizando a exceção

@dataclass(frozen=True)
class Endereco:
    """
    Objeto de Valor para representar um Endereço completo.
    Inclui logradouro, número, complemento (opcional), bairro, CEP e localização (Cidade/Estado).
    """
    logradouro: str = field(metadata={'description': 'Nome da rua, avenida, etc.'})
    numero: str = field(metadata={'description': 'Número do imóvel.'})
    complemento: str | None = field(default=None,
                                    metadata={'description': 'Complemento do endereço (apartamento, sala, etc.).'})
    bairro: str = field(metadata={'description': 'Nome do bairro.'})
    cep: str = field(metadata={'description': 'Código de Endereçamento Postal.'})
    localizacao: Localizacao = field(metadata={'description': 'Objeto de valor de Localização (Cidade e Estado).'})

    def __post_init__(self):
        """
        Validações pós-inicialização para o Objeto de Valor Endereco.
        """
        if not self.logradouro or not self.logradouro.strip():
            raise ErroValidacaoLocalizacao("O logradouro do endereço não pode estar vazio.")
        if not self.numero or not self.numero.strip():
            raise ErroValidacaoLocalizacao("O número do endereço não pode estar vazio.")
        if not self.bairro or not self.bairro.strip():
            raise ErroValidacaoLocalizacao("O bairro do endereço não pode estar vazio.")
        
        # Validação básica de CEP (formato de 8 dígitos numéricos)
        cep_limpo = self.cep.replace('-', '')
        if not re.fullmatch(r'\d{8}', cep_limpo):
            raise ErroValidacaoLocalizacao("O CEP deve conter 8 dígitos numéricos.")
        object.__setattr__(self, 'cep', cep_limpo) # Normaliza o CEP

        # A validação da Localizacao já ocorre em seu próprio __post_init__

    def __str__(self):
        """
        Retorna a representação em string do endereço.
        """
        complemento_str = f" {self.complemento}" if self.complemento else ""
        return f"{self.logradouro}, {self.numero}{complemento_str} - {self.bairro}, {self.localizacao.cidade} - {self.localizacao.estado}, {self.cep}"