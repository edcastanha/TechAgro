from rest_framework import serializers
from .models import ProdutorRural, Endereco

class EnderecoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Endereco
        fields = '__all__'

class ProdutorRuralSerializer(serializers.ModelSerializer):
    # Propriedades é o related_name definido no ForeignKey de Propriedade para ProdutorRural
    propriedades = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = ProdutorRural
        fields = '__all__'
