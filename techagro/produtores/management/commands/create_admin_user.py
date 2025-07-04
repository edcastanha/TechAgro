from django.core.management.base import BaseCommand
from core.models import User

class Command(BaseCommand):
    help = 'Cria um superusuário admin para testes.'

    def handle(self, *args, **options):
        email = 'admin@techagro.com.br'
        username = 'admin'
        password = 'admin123' # Senha padrão para testes

        if not User.objects.filter(email=email).exists():
            User.objects.create_superuser(username=username, email=email, password=password)
            self.stdout.write(self.style.SUCCESS(f'Superusuário {username} ({email}) criado com sucesso!'))
        else:
            self.stdout.write(self.style.WARNING(f'Superusuário {username} ({email}) já existe.'))
