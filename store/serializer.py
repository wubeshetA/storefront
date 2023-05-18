from decimal import Decimal
from rest_framework import serializers
from .models import Product


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title']
        
        
    # id = serializers.IntegerField()
    # title = serializers.CharField(max_length=255)
class ProductSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Product
        fields = [

            'title',
            'description',
            'unit_price',
            'price_with_tax',
            'collection',
        
        ]
        
    """The following fields were added when the serializer was created
    with the Serializer class not ModelSerializer. Now since we have 
    ModelSerializer we don't need them anymore."""
    
    # title = serializers.CharField(max_length=225)
    # description = serializers.CharField(min_length=2, max_length=225)
    # price = serializers.DecimalField(
    #     max_digits=6,
    #     decimal_places=2,
    #     source='unit_price'
    # )
    price_with_tax = serializers.SerializerMethodField(method_name='calculate_tax')
    
    # Adding RelatedField by PrimaryKeyField
    # collection = serializers.PrimaryKeyRelatedField(read_only=True)
    
    # Adding RelatedField by StringField
    # collection = serializers.StringRelatedField()
    
    # Adding RelatedField by NestedSerializer
    # collection = CollectionSerializer()
    
    # Adding RelatedField by HyperlinkedRelatedField
    collection = serializers.HyperlinkedRelatedField(
        view_name='collection-detail',
        read_only=True)
    
    def calculate_tax(self, product: Product):
        return product.unit_price * Decimal(1.1)