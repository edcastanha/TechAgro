from rest_framework import viewsets
from .models import Produtor, Propriedade, Safra, AtividadeRural
from .serializers import (
    ProdutorSerializer,
    PropriedadeSerializer,
    SafraSerializer,
    AtividadeRuralSerializer
)
from helpers.logging_helper import get_logger

logger = get_logger()

# Create your views here.

class ProdutorViewSet(viewsets.ModelViewSet):
    queryset = Produtor.objects.all()
    serializer_class = ProdutorSerializer

    def perform_create(self, serializer):
        try:
            instance = serializer.save()
            logger.info(f"Produtor criado: {instance.nome} (ID: {instance.id})")
        except Exception as e:
            logger.error(f"Erro ao criar produtor: {e}")
            raise

    def perform_update(self, serializer):
        try:
            instance = serializer.save()
            logger.info(f"Produtor atualizado: {instance.nome} (ID: {instance.id})")
        except Exception as e:
            logger.error(f"Erro ao atualizar produtor: {e}")
            raise

    def perform_destroy(self, instance):
        try:
            logger.info(f"Produtor removido: {instance.nome} (ID: {instance.id})")
            instance.delete()
        except Exception as e:
            logger.error(f"Erro ao remover produtor: {e}")
            raise

class PropriedadeViewSet(viewsets.ModelViewSet):
    queryset = Propriedade.objects.all()
    serializer_class = PropriedadeSerializer

    def perform_create(self, serializer):
        try:
            instance = serializer.save()
            logger.info(f"Propriedade criada: {instance.nome_propriedade} (ID: {instance.id})")
        except Exception as e:
            logger.error(f"Erro ao criar propriedade: {e}")
            raise

    def perform_update(self, serializer):
        try:
            instance = serializer.save()
            logger.info(f"Propriedade atualizada: {instance.nome_propriedade} (ID: {instance.id})")
        except Exception as e:
            logger.error(f"Erro ao atualizar propriedade: {e}")
            raise

    def perform_destroy(self, instance):
        try:
            logger.info(f"Propriedade removida: {instance.nome_propriedade} (ID: {instance.id})")
            instance.delete()
        except Exception as e:
            logger.error(f"Erro ao remover propriedade: {e}")
            raise

class SafraViewSet(viewsets.ModelViewSet):
    queryset = Safra.objects.all()
    serializer_class = SafraSerializer

    def perform_create(self, serializer):
        try:
            instance = serializer.save()
            logger.info(f"Safra criada: {instance.ano} - {instance.propriedade.nome_propriedade} (ID: {instance.id})")
        except Exception as e:
            logger.error(f"Erro ao criar safra: {e}")
            raise

    def perform_update(self, serializer):
        try:
            instance = serializer.save()
            logger.info(f"Safra atualizada: {instance.ano} - {instance.propriedade.nome_propriedade} (ID: {instance.id})")
        except Exception as e:
            logger.error(f"Erro ao atualizar safra: {e}")
            raise

    def perform_destroy(self, instance):
        try:
            logger.info(f"Safra removida: {instance.ano} - {instance.propriedade.nome_propriedade} (ID: {instance.id})")
            instance.delete()
        except Exception as e:
            logger.error(f"Erro ao remover safra: {e}")
            raise

class AtividadeRuralViewSet(viewsets.ModelViewSet):
    queryset = AtividadeRural.objects.all()
    serializer_class = AtividadeRuralSerializer

    def perform_create(self, serializer):
        try:
            instance = serializer.save()
            logger.info(f"Atividade Rural criada: {instance.nome_cultura} - Safra {instance.safra.ano} (ID: {instance.id})")
        except Exception as e:
            logger.error(f"Erro ao criar atividade rural: {e}")
            raise

    def perform_update(self, serializer):
        try:
            instance = serializer.save()
            logger.info(f"Atividade Rural atualizada: {instance.nome_cultura} - Safra {instance.safra.ano} (ID: {instance.id})")
        except Exception as e:
            logger.error(f"Erro ao atualizar atividade rural: {e}")
            raise

    def perform_destroy(self, instance):
        try:
            logger.info(f"Atividade Rural removida: {instance.nome_cultura} - Safra {instance.safra.ano} (ID: {instance.id})")
            instance.delete()
        except Exception as e:
            logger.error(f"Erro ao remover atividade rural: {e}")
            raise
