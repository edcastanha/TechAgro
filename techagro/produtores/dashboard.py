from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Sum, Count, F
from .models import Propriedade, AtividadeRural

class DashboardView(APIView):
    """
    Endpoint para fornecer dados agregados para o dashboard.
    """
    def get(self, request):
        # Total de fazendas
        total_fazendas = Propriedade.objects.count()
        # Total de hectares registrados
        total_hectares = Propriedade.objects.aggregate(total=Sum('area_total_hectares'))['total'] or 0
        # Gráfico por estado
        por_estado = (
            Propriedade.objects.values('estado')
            .annotate(qtd=Count('id'))
            .order_by('-qtd')
        )
        # Gráfico por cultura plantada
        por_cultura = (
            AtividadeRural.objects.values('nome_cultura')
            .annotate(qtd=Count('id'))
            .order_by('-qtd')
        )
        # Gráfico por uso do solo
        uso_solo = Propriedade.objects.aggregate(
            total_agricultavel=Sum('area_agricultavel_hectares'),
            total_vegetacao=Sum('area_vegetacao_hectares')
        )
        return Response({
            'total_fazendas': total_fazendas,
            'total_hectares': total_hectares,
            'por_estado': list(por_estado),
            'por_cultura': list(por_cultura),
            'uso_solo': uso_solo,
        }, status=status.HTTP_200_OK)
