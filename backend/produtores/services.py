from django.db.models import Sum, Count
from .models import Propriedade, AtividadeRural

def dashboard_data():
    total_fazendas = Propriedade.objects.count()
    total_hectares = Propriedade.objects.aggregate(total=Sum('area_total_hectares'))['total'] or 0
    por_estado = (
        Propriedade.objects.values('estado')
        .annotate(qtd=Count('id'))
        .order_by('-qtd')
    )
    por_cultura = (
        AtividadeRural.objects.values('nome_cultura')
        .annotate(qtd=Count('id'))
        .order_by('-qtd')
    )
    uso_solo = Propriedade.objects.aggregate(
        total_agricultavel=Sum('area_agricultavel_hectares'),
        total_vegetacao=Sum('area_vegetacao_hectares')
    )
    return {
        'total_fazendas': total_fazendas,
        'total_hectares': total_hectares,
        'por_estado': list(por_estado),
        'por_cultura': list(por_cultura),
        'uso_solo': uso_solo,
    }
