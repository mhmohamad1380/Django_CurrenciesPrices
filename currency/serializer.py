from rest_framework.serializers import ModelSerializer

from currency.models import Currencies


class CurrencySerializer(ModelSerializer):
    class Meta:
        model = Currencies
        fields = '__all__'
