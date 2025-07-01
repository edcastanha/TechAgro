# src/infrastructure/django_app/apps.py

from django.apps import AppConfig
import os
import django

class DjangoAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'src.infrastructure.django_app' # O nome da sua aplicação Django

    def ready(self):
        # Esta função é executada quando a aplicação Django está pronta.
        # Útil para inicializações, mas para o ORM puro, settings.configure já basta.
        pass

# Esta parte é importante para inicializar o Django ORM
# Fora de um projeto Django tradicional (wsgi/asgi)
if not os.environ.get('DJANGO_SETTINGS_MODULE'):
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'src.infrastructure.django_app.settings')
    try:
        django.setup()
    except Exception as e:
        # Se o setup já foi feito ou há outro erro, evita duplicidade
        print(f"Django setup warning: {e}")