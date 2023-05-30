#!/usr/bin/env python3

"""
Models for the store app.
"""
import uuid
from django.db import models
from django.contrib import admin
from django.core.validators import MinValueValidator
# import settings from django auth
from django.conf import settings

from store.validators import validate_image_size

class Promotion(models.Model):
    description = models.CharField(max_length=255)
    discount = models.FloatField()

class Collection(models.Model):
    title = models.CharField(max_length=255)
    # on the following feild the related_name='+' means
    # that we don't need to create a reverse relationship from Collection to Product.
    featured_product = models.ForeignKey(
        'Product', on_delete=models.SET_NULL, null=True, related_name='+')
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['title']
    

class Product(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    description = models.TextField()
    unit_price = models.DecimalField(
        max_digits=6, 
        decimal_places=2,  
        validators=[MinValueValidator(0)])
    inventory = models.IntegerField(
        validators=[MinValueValidator(1)]
    )
    last_update = models.DateTimeField(auto_now=True)
    # Each product belongs to a collection, and each collection can have many products.
    # The following field creates a one-to-many relationship between Collection and Product.
    # if a collection is deleted, all products in that collection will not be deleted.
    collection = models.ForeignKey(Collection, on_delete=models.PROTECT, related_name="products")
    # Each product can have many promotions, and each promotion can have many products.
    # The following field creates a many-to-many relationship between Promotion and Product.
    # you can add a key word argument "related_name" to the ManyToManyField to specify the name of the reverse relationship in the Promotion model. By default, Django will use the name of the model in lowercase, followed by _set. e.g products_set.
    # promotions = models.ManyToManyField(Promotion, related_name="products")
    promotions = models.ManyToManyField(Promotion, )
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['title']
        
class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, 
        on_delete=models.CASCADE,
        related_name="images",
        )
    image = models.ImageField(upload_to="store/images",
                              validators=[validate_image_size]
        )
    
class Customer(models.Model):
    MEMBERSHIP_BRONZE = 'B'
    MEMBERSHIP_SILVER = 'S'
    MEMBERSHIP_GOLD = 'G'

    MEMBERSHIP_CHOICES = [
        (MEMBERSHIP_BRONZE, 'Bronze'),
        (MEMBERSHIP_SILVER, 'Silver'),
        (MEMBERSHIP_GOLD, 'Gold'),
    ]
    # first_name = models.CharField(max_length=255)
    # last_name = models.CharField(max_length=255)
    # email = models.EmailField(unique=True)
    phone = models.CharField(max_length=255)
    birth_date = models.DateField(null=True)
    membership = models.CharField(
        max_length=1, choices=MEMBERSHIP_CHOICES, default=MEMBERSHIP_BRONZE)
    
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    # order_set field will be created automatically because of it's relationship with Order table.
    
    @admin.display(ordering='user__first_name')
    def first_name(self):
        return self.user.first_name

    @admin.display(ordering='user__last_name')
    def last_name(self):
        return self.user.last_name
    
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
    
    class Meta:
        ordering = ['user__first_name', 'user__last_name']

class Order(models.Model):
    PAYMENT_PENDING = 'P'
    PAYMENT_COMPLETE = 'C'
    PAYMENT_FAILED = 'F'
    PAYMENT_STATUS_CHOICES = [
        (PAYMENT_PENDING, 'Pending'),
        (PAYMENT_COMPLETE, 'Complete'),
        (PAYMENT_FAILED, 'Failed'),
    ]
    placed_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=1,
                                      choices=PAYMENT_STATUS_CHOICES,
                                      default=PAYMENT_PENDING)
    # the following field create one-to-many relationship between customer and order
    # if a customer is deleted, the customer's orders will not be deleted (will be protected).
    # Based on the following custormer relationship django will create a field called 'order_set' in the customer model
    # however we can not use order_set as a reference when querying the customer. we have to use just order.
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    
    class Meta:
        permissions = [
            ("cancel_order", "Can cancel order"),
        ]
    
    
    # orderItem_set <--- cuz of the it's relationship with OrderItem
class OrderItem(models.Model):
    # If an order is deleted, OrderItem will not be deleted.
    # I.e, if order has at least one order item, the item will not be deleted.
    order = models.ForeignKey(Order, on_delete=models.PROTECT, related_name='items')
    # if we accidentally delete a product, we don't want to delete the order item.
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='order_items')
    quantity = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, 
                                     decimal_places=2,
                                     validators=[MinValueValidator(0)])

class Address(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    # the following field create one-to-one relationship between Customer and Address
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    
class Cart(models.Model):
    # this field will be autopopulated when a cart is created.
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)


class CartItem(models.Model):
    # If a cart is deleted, CartItem will be also be deleted.
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    # if a product is deleted, CartItem will be also be deleted.
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)]
    )
    
    # make sure that the combination of cart and product is unique.
    class Meta:
        unique_together = ['cart', 'product']
    
class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length=225) # name of the reviewer
    description = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    