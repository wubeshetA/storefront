from decimal import Decimal
from django.db import transaction
from rest_framework import serializers
from .models import Cart, CartItem, Customer, Order, OrderItem, Product, Collection, Review


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'title', 'products_count']
    products_count = serializers.IntegerField(read_only=True)
        # calculate the number of products in the collection
                
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
            'inventory',
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
    
    # collection = serializers.HyperlinkedRelatedField(
    #     view_name='collection-detail',
    #     read_only=True)
    
    def calculate_tax(self, product: Product):
        return product.unit_price * Decimal(1.1)
    
    
    # the following validate method is a method of ModelSerializer class and 
    # it can be overridden to validate data before deserialization
    def validate(self, data):
        if data['title'] == data['description']:
            raise serializers.ValidationError('Title and Description should be different from each other.')
        return data

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'date', 'name', 'description']
        # set product_id atomatically from parent models
        
    def create(self, validated_data):
        # return Review.objects.create(**validated_data)
        # include product_id from context on the above commented line
        return Review.objects.create(product_id=self.context['product_id'], **validated_data)

class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'unit_price']

class CartItemSerializer(serializers.ModelSerializer):

    product = SimpleProductSerializer()
    total_price = serializers.SerializerMethodField() # calculate total price
    
    def get_total_price(self, item: CartItem):
        return item.product.unit_price * item.quantity
    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'total_price']

    def create(self, validated_data):
        # return CartItem.objects.create(**validated_data)
        # include cart_id from context on the above commented line
        return CartItem.objects.create(cart_id=self.context['cart_id'], **validated_data)
    
    
class CartSerializer(serializers.ModelSerializer):
    # make id readonly
    id = serializers.UUIDField(read_only=True)
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField(read_only=True)
    
    def get_total_price(self, cart: Cart):
        return sum ([item.product.unit_price * item.quantity
                     for item in cart.items.all()])
    class Meta:
        model = Cart
        fields = ['id', 'items', 'total_price']


class AddCartItemSerializer(serializers.ModelSerializer):
    
    product_id = serializers.IntegerField()
    
    # validate product_id
    def validate_product_id(self, value):
        try:
            Product.objects.get(id=value)
        except Product.DoesNotExist:
            raise serializers.ValidationError('Product with id {} does not exist'.format(value))
        return value
    class Meta:
        model = CartItem
        fields = ['product_id', 'quantity']
        
    def save(self, **kwargs):
        
        product_id = self.validated_data['product_id']
        quantity = self.validated_data['quantity']
        cart_id = self.context['cart_id']
        
        try:
            cart_item = CartItem.objects.filter(product_id=product_id, cart_id=cart_id).get()
            # update the value of quantity
            cart_item.quantity += quantity
            cart_item.save()
            self.instance = cart_item
        except CartItem.DoesNotExist:
            self.instance = CartItem.objects.create(product_id=product_id, cart_id=cart_id, quantity=quantity)
        return self.instance
    
class UpdateCartItemSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CartItem
        fields = ['quantity']

    def update(self, instance, validated_data):
        instance.quantity = validated_data['quantity']
        instance.save()
        return instance

class CustomerSerializer(serializers.ModelSerializer):
    
    user_id = serializers.IntegerField(read_only=True)
    class Meta:
        model = Customer
        fields = ['id', 'user_id', 'phone', 'birth_date', 'membership']


class OrderItemSerializer(serializers.ModelSerializer):
    
    product = SimpleProductSerializer(read_only=True)
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity']

class OrderSerializer(serializers.ModelSerializer):
    
    items = OrderItemSerializer(many=True, read_only=True)
    class Meta:
        model = Order
        fields = ['id', 'customer', 'placed_at', 'payment_status', 'items']

class CreateOrderSerializer(serializers.Serializer):
    
    cart_id = serializers.UUIDField()
    
    def validate_cart_id(self, value):
        if not Cart.objects.filter(pk=value).exists():
            raise serializers.ValidationError('Cart with id {} does not exist'.format(value))
        elif CartItem.objects.filter(cart_id=value).count() == 0:
            raise serializers.ValidationError('Cart with id {} is empty'.format(value))
        return value
    
    def save(self, **kwargs):
        
        with transaction.atomic():
            cart_id = self.validated_data['cart_id']
            user_id = self.context['user_id']
            # create order
            (customer, created) = Customer.objects.get_or_create(user_id=user_id)
            order = Order.objects.create(customer=customer)
            # create order items from cart item
            cart_items = CartItem.objects.filter(cart_id=cart_id)
            
            # create order_items from cart_items
            order_items = [
                
                OrderItem(
                                order=order,
                                product=cart_item.product,
                                quantity=cart_item.quantity,
                                unit_price=cart_item.product.unit_price)
                for cart_item in cart_items
                ]
            
            # save order_items in bulk
            OrderItem.objects.bulk_create(order_items)
            
            Cart.objects.get(id=cart_id).delete()
            return order
        
class UpdateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['payment_status']
