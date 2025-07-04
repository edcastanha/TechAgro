from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, ProdutorRural, TecnicoAgrícola, AgenteEscritorio, Endereco

# Custom User Admin
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('id',)}), # Adiciona o campo ID ao fieldsets
    )
    readonly_fields = ('id',)

# Register other models
@admin.register(ProdutorRural)
class ProdutorRuralAdmin(admin.ModelAdmin):
    list_display = ('nome', 'documento', 'tipo_documento', 'email')
    search_fields = ('nome', 'documento', 'email')
    list_filter = ('tipo_documento',)

@admin.register(TecnicoAgrícola)
class TecnicoAgrícolaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'registro_profissional')
    search_fields = ('nome', 'email', 'registro_profissional')

@admin.register(AgenteEscritorio)
class AgenteEscritorioAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'departamento')
    search_fields = ('nome', 'email', 'departamento')

@admin.register(Endereco)
class EnderecoAdmin(admin.ModelAdmin):
    list_display = ('cidade', 'estado', 'cep', 'logradouro')
    search_fields = ('cidade', 'estado', 'cep', 'logradouro')