# src/application/use_cases/inativar_produtor_rural.py

from src.core.ports.produtor_repository import IProdutorRepository
from src.core.domain.exceptions.exceptions import ErroDominio
from src.application.dtos.produtor_dtos import InativarProdutorInputDTO, ProdutorStatusOutputDTO

class InativarProdutorRuralUseCase:
    """
    Caso de Uso para inativar um Produtor Rural, alterando seu status 'ativo' para False.
    """
    def __init__(self, produtor_repository: IProdutorRepository):
        """
        Injeta a dependência do repositório de produtores.
        """
        self.produtor_repository: IProdutorRepository = produtor_repository

    def executar(self, input_dto: InativarProdutorInputDTO) -> ProdutorStatusOutputDTO:
        """
        Executa a lógica para inativar um produtor rural.

        Args:
            input_dto: DTO de entrada com o ID do produtor a ser inativado.

        Returns:
            ProdutorStatusOutputDTO: DTO de saída confirmando a inativação.

        Raises:
            ErroDominio: Se o produtor não for encontrado ou já estiver inativo.
        """
        # 1. Busca o produtor existente pelo ID
        produtor_existente = self.produtor_repository.buscar_por_id(input_dto.produtor_id)

        if not produtor_existente:
            raise ErroDominio(f"Produtor com ID '{input_dto.produtor_id}' não encontrado.")
        
        if not produtor_existente.ativo:
            raise ErroDominio(f"Produtor com ID '{input_dto.produtor_id}' já está inativo.")

        # 2. Invoca o método de domínio na entidade para inativar
        produtor_existente.inativar()

        # 3. Persiste a mudança de status através do repositório
        self.produtor_repository.salvar(produtor_existente)

        # 4. Retorna o DTO de saída
        return ProdutorStatusOutputDTO(
            produtor_id=produtor_existente.id,
            ativo=produtor_existente.ativo,
            mensagem=f"Produtor com ID '{produtor_existente.id}' foi inativado com sucesso."
        )

# Opcional: Caso de uso para reativar, seguindo o mesmo padrão
class ReativarProdutorRuralUseCase:
    """
    Caso de Uso para reativar um Produtor Rural, alterando seu status 'ativo' para True.
    """
    def __init__(self, produtor_repository: IProdutorRepository):
        self.produtor_repository: IProdutorRepository = produtor_repository

    def executar(self, input_dto: InativarProdutorInputDTO) -> ProdutorStatusOutputDTO: # Pode usar o mesmo DTO
        produtor_existente = self.produtor_repository.buscar_por_id(input_dto.produtor_id)

        if not produtor_existente:
            raise ErroDominio(f"Produtor com ID '{input_dto.produtor_id}' não encontrado.")
        
        if produtor_existente.ativo:
            raise ErroDominio(f"Produtor com ID '{input_dto.produtor_id}' já está ativo.")

        produtor_existente.reativar()
        self.produtor_repository.salvar(produtor_existente)

        return ProdutorStatusOutputDTO(
            produtor_id=produtor_existente.id,
            ativo=produtor_existente.ativo,
            mensagem=f"Produtor com ID '{produtor_existente.id}' foi reativado com sucesso."
        )