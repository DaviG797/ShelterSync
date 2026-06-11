from rest_framework import serializers
from .models import Instituicao, Acolhido

class InstituicaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instituicao
        fields = '__all__' # O '__all__' avisa para converter todos os campos que existem no modelo

class AcolhidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Acolhido
        fields = '__all__'