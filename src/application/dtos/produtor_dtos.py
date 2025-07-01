# src/application/dtos/produtor_dtos.py

from dataclasses import dataclass, field
from typing import Optional

# DTOs de entrada para criação/atualização de Produtor

@dataclass
class CriarPessoaInputDTO:
    """DTO para os dados de uma Pessoa Física ao criar/atualizar um Produtor."""
    nome: str
    cpf: str # CPF como string no input, será validado e convertido para VO no caso de uso

@dataclass
class CriarEmpresaInputDTO:
    """DTO para os dados de uma Pessoa Jurídica ao criar/atualizar um Produtor."""
    razao_social: str
    cnpj: str # CNPJ como string no input
    nome_fantasia: Optional[str] = None

@dataclass
class CriarProdutorInputDTO:
    """
    DTO de entrada para o caso de uso de criação de Produtor.
    Aceita dados para Pessoa ou Empresa.
    """
    pessoa: Optional[CriarPessoaInputDTO] = None
    empresa: Optional[CriarEmpresaInputDTO] = None

@dataclass
class AtualizarProdutorInputDTO:
    """
    DTO de entrada para o caso de uso de atualização de Produtor.
    Permite atualizar nome/razão social, mas não o documento principal.
    """
    produtor_id: str
    nome: Optional[str] = None # Para Pessoa
    razao_social: Optional[str] = None # Para Empresa
    nome_fantasia: Optional[str] = None # Para Empresa

# DTOs de saída para Produtor

@dataclass
class ProdutorOutputDTO:
    """DTO de saída para representar um Produtor."""
    id: str
    nome: str
    documento: str # CPF ou CNPJ formatado
    tipo: str # "PESSOA_FISICA" ou "PESSOA_JURIDICA" (calculado a partir do ResponsavelLegal)

@dataclass
class InativarProdutorInputDTO:
    """DTO de entrada para o caso de uso de inativação de Produtor."""
    produtor_id: str

@dataclass
class ProdutorStatusOutputDTO:
    """DTO de saída para informar o status de inativação/ativação."""
    produtor_id: str
    ativo: bool
    mensagem: str