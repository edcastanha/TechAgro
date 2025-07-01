# src/application/use_cases/cadastrar_produtor_rural.py (AJUSTADO)

from src.core.ports.produtor_repository import IProdutorRepository
from src.core.domain.entities.produtor import Produtor
from src.core.domain.entities.p
from src.core.domain.entities.responsavel_legal import ResponsavelLegal
from src.core.domain.value_objects.documentos import CPF, CNPJ
from src.core.domain.exceptions.exceptions import ErroValidacaoProdutor, ErroValidacaoDocumento
from src.application.dtos.produtor_dtos import CriarProdutorInputDTO, ProdutorOutputDTO

class CadastrarProdutorRuralUseCase:
    """
    Caso de Uso para cadastrar um novo Produtor Rural (Pessoa Física ou Jurídica).
    """
    def __init__(self, produtor_repository: IProdutorRepository):
        self.produtor_repository: IProdutorRepository = produtor_repository

    def executar(self, input_dto: CriarProdutorInputDTO) -> ProdutorOutputDTO:
        """
        Executa a lógica para cadastrar um produtor rural.

        Args:
            input_dto: DTO de entrada contendo os dados do novo produtor.

        Returns:
            ProdutorOutputDTO: DTO de saída com os dados do produtor cadastrado.

        Raises:
            ErroValidacaoProdutor: Se os dados do produtor forem inválidos.
            ErroValidacaoDocumento: Se o CPF/CNPJ for inválido ou já existir.
        """
        if not input_dto.pessoa and not input_dto.empresa:
            raise ErroValidacaoProdutor("É necessário fornecer dados para Pessoa Física ou Pessoa Jurídica.")
        
        responsavel_legal_a_criar: Optional[ResponsavelLegal] = None
        documento_string: str # Para verificar duplicidade

        if input_dto.pessoa:
            try:
                cpf_vo = CPF(input_dto.pessoa.cpf)
                responsavel_legal_a_criar = Pessoa(nome=input_dto.pessoa.nome, cpf=cpf_vo)
                documento_string = cpf_vo.valor
            except ErroValidacaoDocumento as e:
                raise ErroValidacaoDocumento(f"CPF inválido: {e.mensagem}")
            except ValueError as e: # Captura erros de validação da própria entidade Pessoa
                raise ErroValidacaoProdutor(f"Dados da Pessoa inválidos: {e}")

        elif input_dto.empresa:
            try:
                cnpj_vo = CNPJ(input_dto.empresa.cnpj)
                responsavel_legal_a_criar = Empresa(
                    razao_social=input_dto.empresa.razao_social,
                    cnpj=cnpj_vo,
                    nome_fantasia=input_dto.empresa.nome_fantasia
                )
                documento_string = cnpj_vo.valor
            except ErroValidacaoDocumento as e:
                raise ErroValidacaoDocumento(f"CNPJ inválido: {e.mensagem}")
            except ValueError as e: # Captura erros de validação da própria entidade Empresa
                raise ErroValidacaoProdutor(f"Dados da Empresa inválidos: {e}")
        
        # Verifica duplicidade
        documento_existente = self.produtor_repository.buscar_por_documento(documento_string)
        if documento_existente:
            raise ErroValidacaoDocumento(f"Já existe um produtor cadastrado com o documento: {documento_string}")

        try:
            # Cria a entidade Produtor, passando o responsável legal
            novo_produtor = Produtor(responsavel_legal=responsavel_legal_a_criar)
        except ErroValidacaoProdutor as e:
            raise e
        except ValueError as e:
            raise ErroValidacaoProdutor(f"Erro ao criar entidade Produtor: {e}")

        self.produtor_repository.salvar(novo_produtor)

        return ProdutorOutputDTO(
            id=novo_produtor.id,
            nome=novo_produtor.nome,
            documento=novo_produtor.documento,
            tipo="PESSOA_FISICA" if novo_produtor.eh_pessoa_fisica() else "PESSOA_JURIDICA" # Usa os novos métodos
        )