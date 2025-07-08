import pytest
from django.core.exceptions import ValidationError
from produtores.models import Produtor, Propriedade, Safra, AtividadeRural
from datetime import date

@pytest.mark.django_db
def test_atividade_rural_criacao_valida():
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
    safra = Safra.objects.create(
        propriedade=prop,
        ano=2024,
        data_inicio=date(2024, 1, 1),
        data_fim=date(2024, 12, 31)
    )
    atividade = AtividadeRural(
        safra=safra,
        nome_cultura='Soja',
        area_plantada_hectares=50
    )
    atividade.full_clean()  # Não deve lançar exceção

@pytest.mark.django_db
def test_atividade_rural_nome_cultura_unica_por_safra():
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
    safra = Safra.objects.create(
        propriedade=prop,
        ano=2024,
        data_inicio=date(2024, 1, 1),
        data_fim=date(2024, 12, 31)
    )
    AtividadeRural.objects.create(
        safra=safra,
        nome_cultura='Soja',
        area_plantada_hectares=50
    )
    with pytest.raises(Exception):
        AtividadeRural.objects.create(
            safra=safra,
            nome_cultura='Soja',
            area_plantada_hectares=10
        )
