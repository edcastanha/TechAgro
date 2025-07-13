# Regras de Negócio

Este documento centraliza as principais regras de negócio e validações implementadas na API TechAgro.

## 1. Produtor Rural

### 1.1. Validação de Documento (CPF/CNPJ)
- **Regra:** O documento do produtor deve ser um CPF (11 dígitos numéricos) ou um CNPJ (14 dígitos numéricos) válido.
- **Implementação:**
  - A validação ocorre no método `clean()` do modelo `Produtor` (`produtores/models.py`).
  - O tipo de documento (`CPF` ou `CNPJ`) é inferido automaticamente com base no número de dígitos.
  - São utilizados algoritmos de validação específicos para CPF e CNPJ.
  - **Local:** `produtores/validators.py` (funções `validate_cpf` e `validate_cnpj`).

### 1.2. Unicidade de Documento
- **Regra:** Não podem existir dois produtores com o mesmo número de documento.
- **Implementação:** O campo `documento` no modelo `Produtor` possui a restrição `unique=True`.

## 2. Propriedade Rural

### 2.1. Validação de Áreas
- **Regra:** A soma da área agricultável e da área de vegetação não pode ser maior que a área total da propriedade.
- **Implementação:**
  - A validação ocorre no método `clean()` do modelo `Propriedade` (`produtores/models.py`).
  - **Local:** `produtores/validators.py` (função `validate_areas_propriedade`).

### 2.2. Unicidade da Propriedade
- **Regra:** Um mesmo produtor não pode ter duas propriedades com o mesmo nome.
- **Implementação:** O modelo `Propriedade` possui a restrição `unique_together = ('produtor', 'nome_propriedade')`.

## 3. Safra
- **Regra:** A data de fim de uma safra não pode ser anterior à sua data de início.
- **Implementação:** A validação ocorre no método `clean()` do modelo `Safra` (`produtores/models.py`).