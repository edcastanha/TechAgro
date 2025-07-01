import pytest
from django.core.exceptions import ValidationError
from techagro.produtores.models import Produtor

def test_produtor_cpf_valido(db):
    produtor = Produtor(documento='12345678909', nome='Produtor Teste')
    produtor.clean()  # Não deve lançar exceção
    assert produtor.tipo_documento == 'CPF'

def test_produtor_cnpj_valido(db):
    produtor = Produtor(documento='11222333000181', nome='Empresa Teste')
    produtor.clean()  # Não deve lançar exceção
    assert produtor.tipo_documento == 'CNPJ'

def test_produtor_documento_invalido(db):
    produtor = Produtor(documento='123', nome='Inválido')
    with pytest.raises(ValidationError):
        produtor.clean()
