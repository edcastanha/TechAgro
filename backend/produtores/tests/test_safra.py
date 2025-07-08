import pytest
from django.core.exceptions import ValidationError
from produtores.models import Produtor, Propriedade, Safra
from datetime import date

@pytest.mark.django_db
def test_safra_datas_validas():
    produtor = Produtor.objects.create(documento='12345678909', nome='Produtor Teste')
    prop = Propriedade.objects.create(
        produtor=produtor,
        nome_propriedade='Fazenda Teste',
        area_total_hectares=100,
        area_agricultavel_hectares=60,
        area_vegetacao_hectares=40,
        cidade='Cidade',
        estado='SP'
    )
    safra = Safra(
        propriedade=prop,
        ano=2024,
        data_inicio=date(2024, 1, 1),
        data_fim=date(2024, 12, 31)
    )
    safra.full_clean()  # Não deve lançar exceção

@pytest.mark.django_db
def test_safra_data_fim_sem_inicio():
    produtor = Produtor.objects.create(documento='12345678909', nome='Produtor Teste')
    prop = Propriedade.objects.create(
        produtor=produtor,
        nome_propriedade='Fazenda Teste',
        area_total_hectares=100,
        area_agricultavel_hectares=60,
        area_vegetacao_hectares=40,
        cidade='Cidade',
        estado='SP'
    )
    safra = Safra(
        propriedade=prop,
        ano=2024,
        data_inicio=None,
        data_fim=date(2024, 12, 31)
    )
    with pytest.raises(ValidationError):
        safra.full_clean()
