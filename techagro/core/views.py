from rest_framework import viewsets
from .models import ProdutorRural, Endereco
from .serializers import ProdutorRuralSerializer, EnderecoSerializer
from helpers.logging_helper import get_logger

logger = get_logger()

class ProdutorRuralViewSet(viewsets.ModelViewSet):
    queryset = ProdutorRural.objects.all()
    serializer_class = ProdutorRuralSerializer

    def perform_create(self, serializer):
        try:
            instance = serializer.save()
            logger.info(f"Produtor Rural criado: {instance.nome} (ID: {instance.id})")
        except Exception as e:
            logger.error(f"Erro ao criar produtor rural: {e}")
            raise

    def perform_update(self, serializer):
        try:
            instance = serializer.save()
            logger.info(f"Produtor Rural atualizado: {instance.nome} (ID: {instance.id})")
        except Exception as e:
            logger.error(f"Erro ao atualizar produtor rural: {e}")
            raise

    def perform_destroy(self, instance):
        try:
            logger.info(f"Produtor Rural removido: {instance.nome} (ID: {instance.id})")
            instance.delete()
        except Exception as e:
            logger.error(f"Erro ao remover produtor rural: {e}")
            raise

class EnderecoViewSet(viewsets.ModelViewSet):
    queryset = Endereco.objects.all()
    serializer_class = EnderecoSerializer

    def perform_create(self, serializer):
        try:
            instance = serializer.save()
            logger.info(f"Endereço criado: {instance.id}")
        except Exception as e:
            logger.error(f"Erro ao criar endereço: {e}")
            raise

    def perform_update(self, serializer):
        try:
            instance = serializer.save()
            logger.info(f"Endereço atualizado: {instance.id}")
        except Exception as e:
            logger.error(f"Erro ao atualizar endereço: {e}")
            raise

    def perform_destroy(self, instance):
        try:
            logger.info(f"Endereço removido: {instance.id}")
            instance.delete()
        except Exception as e:
            logger.error(f"Erro ao remover endereço: {e}")
            raise