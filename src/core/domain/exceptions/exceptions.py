class ErroDominio(Exception):
    """
    Exceção base para todos os erros de domínio personalizados.
    Permite capturar qualquer erro relacionado às regras de negócio.
    """
    def __init__(self, mensagem="Ocorreu um erro de domínio inesperado."):
        self.mensagem = mensagem
        super().__init__(self.mensagem)

class ErroValidacaoDocumento(ErroDominio):
    """
    Exceção para erros de validação de documentos (CPF, CNPJ).
    """
    def __init__(self, mensagem="Documento inválido."):
        super().__init__(mensagem)

class ErroValidacaoArea(ErroDominio):
    """
    Exceção para erros de validação de áreas (MedidaArea).
    """
    def __init__(self, mensagem="Área inválida."):
        super().__init__(mensagem)

class ErroValidacaoLocalizacao(ErroDominio):
    """
    Exceção para erros de validação de localização.
    """
    def __init__(self, mensagem="Localização inválida."):
        super().__init__(mensagem)

class ErroValidacaoProdutor(ErroDominio):
    """
    Exceção para erros de validação na entidade Produtor.
    """
    def __init__(self, mensagem="Dados do produtor inválidos."):
        super().__init__(mensagem)

class ErroValidacaoPropriedadeRural(ErroDominio):
    """
    Exceção para erros de validação na entidade Propriedade Rural.
    """
    def __init__(self, mensagem="Dados da propriedade rural inválidos."):
        super().__init__(mensagem)

class ErroValidacaoSafra(ErroDominio):
    """
    Exceção para erros de validação na entidade Safra.
    """
    def __init__(self, mensagem="Dados da safra inválidos."):
        super().__init__(mensagem)

class ErroValidacaoAtividadeRural(ErroDominio):
    """
    Exceção para erros de validação na entidade Atividade Rural.
    """
    def __init__(self, mensagem="Dados da atividade rural inválidos."):
        super().__init__(mensagem)