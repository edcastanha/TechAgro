# produtores/admin.py

from django.contrib import admin
from .models import Produtor, Propriedade, Safra, AtividadeRural


class ProdutorAdmin(admin.ModelAdmin):
    list_display = ('nome', 'documento', 'tipo_documento')
    search_fields = ('nome', 'documento')
    fieldsets = (
        (None, {
            'fields': ('nome', 'documento', 'tipo_documento')
        }),
    )


class PropriedadeAdmin(admin.ModelAdmin):
    list_display = ('nome_propriedade', 'produtor', 'cidade', 'estado', 'area_total_hectares')
    list_filter = ('estado', 'cidade')
    search_fields = ('nome_propriedade', 'produtor__nome', 'produtor__documento')
    fieldsets = (
        (None, {
            'fields': ('produtor', 'nome_propriedade')
        }),
        ('Localização', {
            'fields': ('cidade', 'estado', 'cep', 'logradouro', 'numero', 'complemento', 'bairro', 'latitude', 'longitude')
        }),
        ('Áreas em Hectares', {
            'fields': ('area_total_hectares', 'area_agricultavel_hectares', 'area_vegetacao_hectares')
        }),
        ('Atividade', {
            'fields': ('tipo_atividade',)
        }),
    )

class SafraAdmin(admin.ModelAdmin):
    list_display = ('ano', 'propriedade', 'descricao')
    list_filter = ('ano',)
    search_fields = ('propriedade__nome_propriedade', 'ano')

class AtividadeRuralAdmin(admin.ModelAdmin):
    list_display = ('nome_cultura', 'safra', 'area_plantada_hectares')
    list_filter = ('nome_cultura', 'safra__ano')
    search_fields = ('nome_cultura', 'safra__propriedade__nome_propriedade')

admin.site.register(Produtor, ProdutorAdmin)
admin.site.register(Propriedade, PropriedadeAdmin)
admin.site.register(Safra, SafraAdmin)
admin.site.register(AtividadeRural, AtividadeRuralAdmin)