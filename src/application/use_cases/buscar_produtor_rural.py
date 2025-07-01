# src/application/use_cases/buscar_produtor_rural.py

from src.core.ports.produtor_repository import IProdutorRepository
from src.core.domain.exceptions.exceptions import ErroDominio, ErroValidacaoDocumento
from src.application.dtos.produtor_dtos import (
    BuscarProdutorPorIdInputDTO,
    BuscarProdutorPorDocumentoInputDTO,
    ProdutorOutputDTO,
    ListarProdutoresOutputDTO
)
from src.core.domain.value_objects.documentos import CPF, CNPJ # Para validação de formato do documento

class BuscarProdutorRuralUseCase:
    """
    Caso de Uso para buscar Produtores Rurais por ID, documento (CPF/CNPJ) ou listar todos.
    """
    def __init__(self, produtor_repository: IProdutorRepository):
        """
        Injeta a dependência do repositório de produtores.
        """
        self.produtor_repository: IProdutorRepository = produtor_repository

    def buscar_por_id(self, input_dto: BuscarProdutorPorIdInputDTO) -> ProdutorOutputDTO:
        """
        Busca um produtor rural pelo seu ID.

        Args:
            input_dto: DTO de entrada com o ID do produtor.

        Returns:
            ProdutorOutputDTO: DTO de saída com os dados do produtor encontrado.

        Raises:
            ErroDominio: Se o produtor não for encontrado.
        """
        produtor = self.produtor_repository.buscar_por_id(input_dto.produtor_id)
        if not produtor:
            raise ErroDominio(f"Produtor com ID '{input_dto.produtor_id}' não encontrado.")
        
        return ProdutorOutputDTO(
            id=produtor.id,
            nome=produtor.nome,
            documento=produtor.documento,
            tipo="PESSOA_FISICA" if produtor.eh_pessoa_fisica() else "PESSOA_JURIDICA"
        )

    def buscar_por_documento(self, input_dto: BuscarProdutorPorDocumentoInputDTO) -> ProdutorOutputDTO:
        """
        Busca um produtor rural pelo seu documento (CPF/CNPJ).

        Args:
            input_dto: DTO de entrada com o documento (CPF ou CNPJ).

        Returns:
            ProdutorOutputDTO: DTO de saída com os dados do produtor encontrado.

        Raises:
            ErroValidacaoDocumento: Se o formato do documento for inválido.
            ErroDominio: Se o produtor não for encontrado.
        """
        documento_limpo = input_dto.documento.replace('-', '').replace('.', '').replace('/', '')

        # Validação básica de formato para saber se é CPF ou CNPJ antes de buscar
        if len(documento_limpo) == 11:
            try:
                CPF(documento_limpo) # Tenta criar o VO para validar o formato
            except ErroValidacaoDocumento as e:
                raise ErroValidacaoDocumento(f"Formato de CPF inválido: {e.mensagem}")
        elif len(documento_limpo) == 14:
            try:
                CNPJ(documento_limpo) # Tenta criar o VO para validar o formato
            except ErroValidacaoDocumento as e:
                raise ErroValidacaoDocumento(f"Formato de CNPJ inválido: {e.mensagem}")
        else:
            raise ErroValidacaoDocumento("Documento deve ser um CPF (11 dígitos) ou CNPJ (14 dígitos).")

        produtor = self.produtor_repository.buscar_por_documento(documento_limpo)
        if not produtor:
            raise ErroDominio(f"Produtor com documento '{documento_limpo}' não encontrado.")
        
        return ProdutorOutputDTO(
            id=produtor.id,
            nome=produtor.nome,
            documento=produtor.documento,
            tipo="PESSOA_FISICA" if produtor.eh_pessoa_fisica() else "PESSOA_JURIDICA"
        )

    def listar_todos(self) -> ListarProdutoresOutputDTO:
        """
        Lista todos os produtores rurais cadastrados.

        Returns:
            ListarProdutoresOutputDTO: DTO de saída contendo uma lista de produtores.
        """
        produtores = self.produtor_repository.buscar_todos()
        produtores_dto = [
            ProdutorOutputDTO(
                id=p.id,
                nome=p.nome,
                documento=p.documento,
                tipo="PESSOA_FISICA" if p.eh_pessoa_fisica() else "PESSOA_JURIDICA"
            ) for p in produtores
        ]
        return ListarProdutoresOutputDTO(produtores=produtores_dto)