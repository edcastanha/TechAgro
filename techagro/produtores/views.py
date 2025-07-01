from django.shortcuts import render
from rest_framework import viewsets
from .models import Produtor, Propriedade, Safra, AtividadeRural
from .serializers import (
    ProdutorSerializer,
    PropriedadeSerializer,
    SafraSerializer,
    AtividadeRuralSerializer
)

# Create your views here.

class ProdutorViewSet(viewsets.ModelViewSet):
    queryset = Produtor.objects.all()
    serializer_class = ProdutorSerializer

class PropriedadeViewSet(viewsets.ModelViewSet):
    queryset = Propriedade.objects.all()
    serializer_class = PropriedadeSerializer

class SafraViewSet(viewsets.ModelViewSet):
    queryset = Safra.objects.all()
    serializer_class = SafraSerializer

class AtividadeRuralViewSet(viewsets.ModelViewSet):
    queryset = AtividadeRural.objects.all()
    serializer_class = AtividadeRuralSerializer
