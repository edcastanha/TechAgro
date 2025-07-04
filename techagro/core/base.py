import uuid
from django.db import models

class BaseModel(models.Model):
    """
    Classe base para modelos, pode ser usada para adicionar campos comuns no futuro.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, help_text="Data e hora de criação do registro.")
    updated_at = models.DateTimeField(auto_now=True, help_text="Data e hora da última atualização do registro.")
    class Meta:
        abstract = True
