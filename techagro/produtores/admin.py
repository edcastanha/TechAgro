# produtores/admin.py

from django.contrib import admin
from .models import Produtor, Propriedade, Safra, AtividadeRural


class ProdutorAdmin(admin.ModelAdmin):
    list_display = ('nome', 'documento', 'email', 'telefone')
    search_fields = ('nome', 'documento')
    # Adicionando um fieldset para organizar os campos no formulário de edição
    fieldsets = (
        (None, {
            'fields': ('nome', 'documento', 'email', 'telefone')
        }),
        ('Informações Adicionais', {
            'fields': ('endereco',)
        }),
    )


class PropriedadeAdmin(admin.ModelAdmin):
    list_display = ('nome_propriedade', 'produtor', 'cidade', 'estado', 'area_total_hectares')
    list_filter = ('estado', 'cidade')
    search_fields = ('nome_propriedade', 'produtor__nome', 'produtor__documento')
    # Adicionando um fieldset para organizar os campos no formulário de edição
    fieldsets = (
        (None, {
            'fields': ('produtor', 'nome_propriedade')
        }),
        ('Localização', {
            'fields': ('cidade', 'estado')
        }),
        ('Áreas em Hectares', {
            'fields': ('area_total_hectares', 'area_agricultavel_hectares', 'area_vegetacao_hectares')
        }),
    )

class SafraAdmin(admin.ModelAdmin):
    list_display = ('ano', 'fazenda', 'descricao')
    list_filter = ('ano',)
    search_fields = ('fazenda__nome_propriedade', 'ano')

class AtividadeRuralAdmin(admin.ModelAdmin):
    list_display = ('nome_cultura', 'safra', 'area_plantada_hectares')
    list_filter = ('nome_cultura', 'safra__ano')
    search_fields = ('nome_cultura', 'safra__fazenda__nome_propriedade')

admin.site.register(Produtor)
admin.site.register(Propriedade, PropriedadeAdmin)
admin.site.register(Safra, SafraAdmin)
admin.site.register(AtividadeRural, AtividadeRuralAdmin)