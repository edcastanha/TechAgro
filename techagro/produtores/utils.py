import re

from django.forms import ValidationError


def validate_cpf(cpf):
    """
    Valida um CPF. Exemplo simplificado, para uma validação robusta,
    considere bibliotecas como 'django-cpf-cnpj'.
    """
    cpf = re.sub(r'[^0-9]', '', cpf) # Remove caracteres não numéricos
    if len(cpf) != 11:
        raise ValidationError('CPF deve ter 11 dígitos.')
    # Lógica de validação de dígitos verificadores (omiti para brevidade, mas seria aqui)
    # Exemplo: if not CpfCnpjValidator().validate_cpf(cpf): raise ValidationError(...)
    return cpf

def validate_cnpj(cnpj):
    """
    Valida um CNPJ. Exemplo simplificado, para uma validação robusta,
    considere bibliotecas como 'django-cpf-cnpj'.
    """
    cnpj = re.sub(r'[^0-9]', '', cnpj) # Remove caracteres não numéricos
    if len(cnpj) != 14:
        raise ValidationError('CNPJ deve ter 14 dígitos.')
    # Lógica de validação de dígitos verificadores (omiti para brevidade, mas seria aqui)
    # Exemplo: if not CpfCnpjValidator().validate_cpf(cpf): raise ValidationError(...)
    return cnpj

# Validador para garantir que a soma das áreas agricultável e vegetação não excede a área total
def validate_areas_Propriedade(area_total, area_agricultavel, area_vegetacao):
    if (area_agricultavel is not None and area_vegetacao is not None and area_total is not None):
        if (area_agricultavel + area_vegetacao) > area_total:
            raise ValidationError(
                'A soma da área agricultável e de vegetação não pode exceder a área total da Propriedade.'
            )

def valida_documento(documento):
    """
    Valida o documento (CPF ou CNPJ) e infere o tipo baseado no número de dígitos.
    """
    documento = re.sub(r'[^0-9]', '', documento)  # Remove caracteres não numéricos
    if len(documento) == 11:
        return validate_cpf(documento)
    elif len(documento) == 14:
        return validate_cnpj(documento)
    else:
        raise ValidationError('Documento deve ter 11 dígitos (CPF) ou 14 dígitos (CNPJ).')