from django.core.management.base import BaseCommand
from techagro.produtores.models import Produtor, Propriedade, Safra, AtividadeRural
from random import randint, choice
from datetime import date

class Command(BaseCommand):
    help = 'Popula o banco com dados mock para testes e demonstração.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('Removendo dados antigos...'))
        AtividadeRural.objects.all().delete()
        Safra.objects.all().delete()
        Propriedade.objects.all().delete()
        Produtor.objects.all().delete()

        self.stdout.write(self.style.SUCCESS('Criando produtores...'))
        produtores = []
        for i in range(3):
            produtor = Produtor.objects.create(
                documento=f'{randint(10000000000, 99999999999)}',
                nome=f'Produtor {i+1}'
            )
            produtores.append(produtor)

        cidades_estados = [
            ("Ribeirão Preto", "SP"),
            ("Uberlândia", "MG"),
            ("Cascavel", "PR")
        ]
        self.stdout.write(self.style.SUCCESS('Criando propriedades...'))
        propriedades = []
        for i, produtor in enumerate(produtores):
            for j in range(2):
                cidade, estado = choice(cidades_estados)
                prop = Propriedade.objects.create(
                    produtor=produtor,
                    nome_propriedade=f'Fazenda {i+1}-{j+1}',
                    area_total_hectares=randint(80, 200),
                    area_agricultavel_hectares=randint(40, 100),
                    area_vegetacao_hectares=randint(20, 60),
                    cidade=cidade,
                    estado=estado
                )
                propriedades.append(prop)

        self.stdout.write(self.style.SUCCESS('Criando safras e culturas...'))
        culturas = ["Soja", "Milho", "Café", "Algodão"]
        for prop in propriedades:
            for ano in [2023, 2024]:
                safra = Safra.objects.create(
                    propriedade=prop,
                    ano=ano,
                    data_inicio=date(ano, 1, 1),
                    data_fim=date(ano, 12, 31)
                )
                for cultura in culturas:
                    if randint(0, 1):
                        AtividadeRural.objects.create(
                            safra=safra,
                            nome_cultura=cultura,
                            area_plantada_hectares=randint(10, 60)
                        )
        self.stdout.write(self.style.SUCCESS('Base populada com sucesso!'))
