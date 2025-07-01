# src/infrastructure/repositories/produtor_django_repository.py

from src.core.ports.produtor_repository import IProdutorRepository
from src.core.domain.entities.produtor import Produtor, Pessoa, Empresa
from src.core.domain.entities.responsavel_legal import ResponsavelLegal
from src.core.domain.value_objects.documentos import CPF, CNPJ
from src.core.domain.exceptions.exceptions import ErroDominio, ErroValidacaoDocumento

from src.infrastructure.django_app.models import ProdutorModel, PessoaModel, EmpresaModel
from src.infrastructure.django_app.models import PropriedadeRuralModel # Para o método de buscar propriedades

from typing import Optional, List

class ProdutorDjangoRepository(IProdutorRepository):
    """
    Implementação concreta da interface IProdutorRepository usando o Django ORM.
    Responsável por mapear entre entidades de domínio Produtor e modelos Django.
    """

    def _to_domain_entity(self, model: ProdutorModel) -> Produtor:
        """
        Converte um ProdutorModel (modelo Django) para uma entidade de domínio Produtor.
        """
        responsavel_legal_domain: ResponsavelLegal

        if model.pessoa:
            cpf_vo = CPF(model.pessoa.cpf) # Reconstroi o Value Object
            responsavel_legal_domain = Pessoa(
                id=str(model.pessoa.id), # Preserve o ID do Responsável Legal do DB
                nome=model.pessoa.nome,
                cpf=cpf_vo
            )
        elif model.empresa:
            cnpj_vo = CNPJ(model.empresa.cnpj) # Reconstroi o Value Object
            responsavel_legal_domain = Empresa(
                id=str(model.empresa.id), # Preserve o ID do Responsável Legal do DB
                razao_social=model.empresa.razao_social,
                cnpj=cnpj_vo,
                nome_fantasia=model.empresa.nome_fantasia
            )
        else:
            raise ErroDominio(f"ProdutorModel {model.id} não possui Pessoa nem Empresa associada.")

        return Produtor(
            id=str(model.id),
            responsavel_legal=responsavel_legal_domain,
            ativo=model.ativo
        )

    def _to_django_model(self, entity: Produtor) -> ProdutorModel:
        """
        Converte uma entidade de domínio Produtor para um ProdutorModel (modelo Django).
        Cria ou atualiza PessoaModel/EmpresaModel aninhados.
        """
        produtor_model: ProdutorModel

        try:
            produtor_model = ProdutorModel.objects.get(id=entity.id)
        except ProdutorModel.DoesNotExist:
            produtor_model = ProdutorModel(id=entity.id) # Novo modelo

        if entity.eh_pessoa_fisica():
            pessoa_entity = entity.responsavel_legal
            try:
                pessoa_model = PessoaModel.objects.get(id=pessoa_entity.id)
                pessoa_model.nome = pessoa_entity.nome
                pessoa_model.cpf = pessoa_entity.obter_documento_principal().valor
            except PessoaModel.DoesNotExist:
                pessoa_model = PessoaModel(
                    id=pessoa_entity.id,
                    nome=pessoa_entity.nome,
                    cpf=pessoa_entity.obter_documento_principal().valor
                )
            pessoa_model.save()
            produtor_model.pessoa = pessoa_model
            produtor_model.empresa = None # Garante que a relação de empresa é nula

        elif entity.eh_pessoa_juridica():
            empresa_entity = entity.responsavel_legal
            try:
                empresa_model = EmpresaModel.objects.get(id=empresa_entity.id)
                empresa_model.razao_social = empresa_entity.razao_social
                empresa_model.cnpj = empresa_entity.obter_documento_principal().valor
                empresa_model.nome_fantasia = empresa_entity.nome_fantasia
            except EmpresaModel.DoesNotExist:
                empresa_model = EmpresaModel(
                    id=empresa_entity.id,
                    razao_social=empresa_entity.razao_social,
                    cnpj=empresa_entity.obter_documento_principal().valor,
                    nome_fantasia=empresa_entity.nome_fantasia
                )
            empresa_model.save()
            produtor_model.empresa = empresa_model
            produtor_model.pessoa = None # Garante que a relação de pessoa é nula
        else:
            raise ErroDominio("Tipo de responsável legal desconhecido ou inválido para mapeamento.")

        produtor_model.ativo = entity.ativo
        
        return produtor_model

    def salvar(self, produtor: Produtor) -> None:
        """
        Salva uma entidade Produtor (cria ou atualiza) no banco de dados.
        """
        django_model = self._to_django_model(produtor)
        django_model.save()

    def buscar_por_id(self, produtor_id: str) -> Optional[Produtor]:
        """
        Busca um produtor pelo seu ID no banco de dados.
        """
        try:
            produtor_model = ProdutorModel.objects.get(id=produtor_id)
            return self._to_domain_entity(produtor_model)
        except ProdutorModel.DoesNotExist:
            return None

    def buscar_todos(self) -> List[Produtor]:
        """
        Busca todos os produtores no banco de dados.
        """
        produtor_models = ProdutorModel.objects.all()
        return [self._to_domain_entity(model) for model in produtor_models]

    def buscar_por_documento(self, documento: str) -> Optional[Produtor]:
        """
        Busca um produtor pelo CPF ou CNPJ no banco de dados.
        """
        try:
            # Tenta buscar por CPF ou CNPJ nos respectivos modelos
            if len(documento) == 11:
                pessoa_model = PessoaModel.objects.get(cpf=documento)
                # Assume que um ProdutorModel sempre existe para uma PessoaModel/EmpresaModel
                # devido ao OneToOneField
                produtor_model = ProdutorModel.objects.get(pessoa=pessoa_model)
                return self._to_domain_entity(produtor_model)
            elif len(documento) == 14:
                empresa_model = EmpresaModel.objects.get(cnpj=documento)
                produtor_model = ProdutorModel.objects.get(empresa=empresa_model)
                return self._to_domain_entity(produtor_model)
            else:
                # O ErroValidacaoDocumento já deve ter pego isso na camada de aplicação,
                # mas é um fallback.
                raise ErroValidacaoDocumento("Formato de documento inválido para busca.")
        except (PessoaModel.DoesNotExist, EmpresaModel.DoesNotExist, ProdutorModel.DoesNotExist):
            return None

    def buscar_propriedades_do_produtor(self, produtor_id: str) -> List[PropriedadeRural]:
        """
        Busca todas as propriedades rurais associadas a um produtor.
        Esta é uma operação que atravessa um agregado e retorna uma lista de entidades.
        Você precisará de um PropriedadeRuralDjangoRepository ou helper para converter.
        Por enquanto, vamos apenas mockar o retorno ou retornar vazio, pois ainda não mapeamos PropriedadeRural.
        """
        # IMPORTANTE: A implementação completa para PropriedadeRural virá depois.
        # Por enquanto, apenas um placeholder para cumprir a interface.
        # No futuro, aqui você carregaria os modelos Django de Propriedade
        # e os converteria para entidades de domínio.
        from src.core.domain.entities.propriedade_rural import PropriedadeRural # Importe aqui para evitar circularidade

        try:
            produtor_model = ProdutorModel.objects.get(id=produtor_id)
            # Para cada PropriedadeRuralModel relacionada, você precisaria convertê-la
            # para uma entidade de domínio PropriedadeRural.
            # Isso geralmente é feito por um helper ou por outro repositório.
            
            # Exemplo (você implementará o _to_domain_entity para PropriedadeRural depois)
            # propriedades_models = produtor_model.propriedades.all()
            # return [PropriedadeRuralDjangoRepository()._to_domain_entity(p_model) for p_model in propriedades_models]
            return [] # Placeholder por enquanto
        except ProdutorModel.DoesNotExist:
            return [] # Se o produtor não existe, não tem propriedades