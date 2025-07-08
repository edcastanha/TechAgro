import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from backend.produtores.models import Produtor

@pytest.mark.django_db
def test_criar_produtor_api():
    client = APIClient()
    data = {"documento": "12345678909", "nome": "Produtor API"}
    response = client.post(reverse('produtor-list'), data)
    assert response.status_code == 201
    assert response.data["nome"] == "Produtor API"

@pytest.mark.django_db
def test_dashboard_api():
    client = APIClient()
    url = reverse('dashboard')
    response = client.get(url)
    assert response.status_code == 200
    assert "total_fazendas" in response.data
