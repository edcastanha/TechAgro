from django.core.management.base import BaseCommand
from produtores.models import Propriedade, Safra, AtividadeRural
from core.models import ProdutorRural, Endereco
from random import randint, choice
from datetime import date

class Command(BaseCommand):
    help = 'Popula o banco com dados mock para testes e demonstração.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('Removendo dados antigos...'))
        AtividadeRural.objects.all().delete()
        Safra.objects.all().delete()
        Propriedade.objects.all().delete()
        ProdutorRural.objects.all().delete()
        Endereco.objects.all().delete()

        self.stdout.write(self.style.SUCCESS('Criando produtores...'))
        produtores = []
        # CPFs e CNPJs válidos para mock
        cpfs_validos = [
            '12345678909',  # válido
            '39053344705',  # válido
            '11144477735'   # válido
        ]
        cnpjs_validos = [
            '11444777000161',  # válido
            '19131243000197',  # válido
            '48729147000109'   # válido
        ]
        for i in range(3):
            if i % 2 == 0:
                produtor = ProdutorRural.objects.create(
                    documento=cpfs_validos[i],
                    nome=f'Produtor {i+1} (CPF)',
                    email=f'produtor{i+1}@example.com'
                )
            else:
                produtor = ProdutorRural.objects.create(
                    documento=cnpjs_validos[i],
                    nome=f'Produtor {i+1} (CNPJ)',
                    email=f'produtor{i+1}@example.com'
                )
            produtores.append(produtor)

        cidades_estados = [
            ("Ribeirão Preto", "SP"),
            ("Uberlândia", "MG"),
            ("Quixadá", "CE")
        ]
        self.stdout.write(self.style.SUCCESS('Criando propriedades...'))
        propriedades = []
        for i, produtor in enumerate(produtores):
            for j in range(2):
                cidade, estado = choice(cidades_estados)
                area_total = randint(80, 200)
                area_agricultavel = randint(20, area_total - 20)
                area_vegetacao = randint(0, area_total - area_agricultavel)
                # Garantir a soma das áreas
                if area_agricultavel + area_vegetacao > area_total:
                    area_vegetacao = area_total - area_agricultavel
                
                endereco = Endereco.objects.create(
                    cidade=cidade,
                    estado=estado
                )

                prop = Propriedade.objects.create(
                    produtor=produtor,
                    endereco=endereco,
                    nome_propriedade=f'Fazenda {i+1}-{j+1}',
                    area_total_hectares=area_total,
                    area_agricultavel_hectares=area_agricultavel,
                    area_vegetacao_hectares=area_vegetacao
                )
                propriedades.append(prop)

        self.stdout.write(self.style.SUCCESS('Criando safras e culturas...'))
        culturas = ["Soja", "Milho", "Café", "Algodão", "Cacau"]
        for prop in propriedades:
            for ano in [2023, 2024, 2025]:
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
