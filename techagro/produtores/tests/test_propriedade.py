import pytest
from django.core.exceptions import ValidationError
from produtores.models import Produtor, Propriedade

@pytest.mark.django_db
def test_propriedade_areas_validas():
    produtor = Produtor.objects.create(documento='12345678909', nome='Produtor Teste')
    prop = Propriedade(
        produtor=produtor,
        nome_propriedade='Fazenda Teste',
        area_total_hectares=100,
        area_agricultavel_hectares=60,
        area_vegetacao_hectares=40,
        cidade='Cidade',
        estado='SP'
    )
    prop.clean()  # Não deve lançar exceção

@pytest.mark.django_db
def test_propriedade_areas_invalidas():
    produtor = Produtor.objects.create(documento='12345678909', nome='Produtor Teste')
    prop = Propriedade(
        produtor=produtor,
        nome_propriedade='Fazenda Teste',
        area_total_hectares=100,
        area_agricultavel_hectares=80,
        area_vegetacao_hectares=30,
        cidade='Cidade',
        estado='SP'
    )
    with pytest.raises(ValidationError):
        prop.clean()
