import re
from django.core.exceptions import ValidationError

def validate_cpf(value):
    cpf = re.sub(r'[^0-9]', '', value)
    if len(cpf) != 11:
        raise ValidationError({'documento': 'CPF deve ter 11 dígitos.'})
    if cpf == cpf[0] * 11:
        raise ValidationError({'documento': 'CPF inválido (todos os dígitos iguais).'})
    for i in range(9, 11):
        soma = sum(int(cpf[num]) * ((i+1) - num) for num in range(0, i))
        digito = ((soma * 10) % 11) % 10
        if digito != int(cpf[i]):
            raise ValidationError({'documento': 'CPF inválido.'})
    return value

def validate_cnpj(value):
    cnpj = re.sub(r'[^0-9]', '', value)
    if len(cnpj) != 14:
        raise ValidationError({'documento': 'CNPJ deve ter 14 dígitos.'})
    if cnpj == cnpj[0] * 14:
        raise ValidationError({'documento': 'CNPJ inválido (todos os dígitos iguais).' })
    pesos1 = [5,4,3,2,9,8,7,6,5,4,3,2]
    pesos2 = [6] + pesos1
    for i, pesos in enumerate([pesos1, pesos2]):
        soma = sum(int(cnpj[num]) * pesos[num] for num in range(len(pesos)))
        digito = 11 - soma % 11
        if digito >= 10:
            digito = 0
        if digito != int(cnpj[12 + i]):
            raise ValidationError({'documento': 'CNPJ inválido.'})
    return value

def validate_areas_propriedade(area_total, area_agricultavel, area_vegetacao):
    if (area_agricultavel is not None and area_vegetacao is not None and area_total is not None):
        if (area_agricultavel + area_vegetacao) > area_total:
            raise ValidationError({
                'area_agricultavel_hectares': 'A soma da área agricultável e de vegetação não pode exceder a área total da Propriedade.',
                'area_vegetacao_hectares': 'A soma da área agricultável e de vegetação não pode exceder a área total da Propriedade.'
            })
