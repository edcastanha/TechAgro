from rest_framework import serializers
from .models import Propriedade, Safra, AtividadeRural

class AtividadeRuralSerializer(serializers.ModelSerializer):
    class Meta:
        model = AtividadeRural
        fields = '__all__'

class SafraSerializer(serializers.ModelSerializer):
    culturas_plantadas = AtividadeRuralSerializer(many=True, read_only=True)

    class Meta:
        model = Safra
        fields = '__all__'

class PropriedadeSerializer(serializers.ModelSerializer):
    safras = SafraSerializer(many=True, read_only=True)

    class Meta:
        model = Propriedade
        fields = '__all__'

 