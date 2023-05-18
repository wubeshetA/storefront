from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=225)
    description = serializers.CharField(min_length=2, max_length=225)
    unit_price = serializers.DecimalField(
        max_digits=6,
        decimal_places=2,
    )