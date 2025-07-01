# src/application/use_cases/atualizar_produtor_rural.py

from src.core.ports.produtor_repository import IProdutorRepository
from src.core.domain.entities.produtor import Produtor
from src.core.domain.exceptions.exceptions import ErroValidacaoProdutor, ErroDominio
from src.application.dtos.produtor_dtos import AtualizarProdutorInputDTO, ProdutorOutputDTO

class AtualizarProdutorRuralUseCase:
    """
    Caso de Uso para atualizar os dados de um Produtor Rural existente.
    Permite atualizar o nome/razão social e nome fantasia.
    """
    def __init__(self, produtor_repository: IProdutorRepository):
        """
        Injeta a dependência do repositório de produtores.
        """
        self.produtor_repository: IProdutorRepository = produtor_repository

    def executar(self, input_dto: AtualizarProdutorInputDTO) -> ProdutorOutputDTO:
        """
        Executa a lógica para atualizar um produtor rural.

        Args:
            input_dto: DTO de entrada contendo o ID do produtor e os dados a serem atualizados.

        Returns:
            ProdutorOutputDTO: DTO de saída com os dados do produtor atualizado.

        Raises:
            ErroDominio: Se o produtor não for encontrado.
            ErroValidacaoProdutor: Se os dados para atualização forem inválidos.
        """
        # 1. Busca o produtor existente pelo ID
        produtor_existente = self.produtor_repository.buscar_por_id(input_dto.produtor_id)

        if not produtor_existente:
            raise ErroDominio(f"Produtor com ID '{input_dto.produtor_id}' não encontrado.")
        
        # 2. Atualiza os dados do Responsável Legal dentro da entidade Produtor
        try:
            if produtor_existente.eh_pessoa_fisica():
                if input_dto.nome is not None:
                    produtor_existente.responsavel_legal.nome = input_dto.nome # Atualiza o atributo da entidade Pessoa
                    # Re-validação da entidade Pessoa após a mudança
                    if not produtor_existente.responsavel_legal.nome.strip():
                        raise ErroValidacaoProdutor("O nome da pessoa não pode ser vazio.")

            elif produtor_existente.eh_pessoa_juridica():
                if input_dto.razao_social is not None:
                    produtor_existente.responsavel_legal.razao_social = input_dto.razao_social # Atualiza a Razão Social
                    if not produtor_existente.responsavel_legal.razao_social.strip():
                        raise ErroValidacaoProdutor("A razão social da empresa não pode ser vazia.")
                if input_dto.nome_fantasia is not None:
                    produtor_existente.responsavel_legal.nome_fantasia = input_dto.nome_fantasia # Atualiza o Nome Fantasia
            else:
                # Caso de um estado inesperado para o tipo de produtor
                raise ErroValidacaoProdutor("Tipo de produtor inválido para atualização.")
        except ValueError as e:
            # Captura exceções de validação que podem surgir da entidade Pessoa/Empresa
            raise ErroValidacaoProdutor(f"Erro de validação ao atualizar dados do responsável legal: {e}")


        # 3. Persiste as mudanças na entidade Produtor (o repositório fará o mapeamento)
        self.produtor_repository.salvar(produtor_existente)

        # 4. Retorna o DTO de saída com os dados atualizados
        return ProdutorOutputDTO(
            id=produtor_existente.id,
            nome=produtor_existente.nome,
            documento=produtor_existente.documento,
            tipo="PESSOA_FISICA" if produtor_existente.eh_pessoa_fisica() else "PESSOA_JURIDICA"
        )