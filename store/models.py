#!/usr/bin/env python3

"""
Models for the store app.
"""
from django.db import models
from django.core.validators import MinValueValidator

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
    description = models.TextField(null=True, blank=True)
    unit_price = models.DecimalField(
        max_digits=6, 
        decimal_places=2, 
        null=True, 
        validators=[MinValueValidator(1)])
    inventory = models.IntegerField(
        validators=[MinValueValidator(0)]
    )
    last_update = models.DateTimeField(auto_now=True)
    # Each product belongs to a collection, and each collection can have many products.
    # The following field creates a one-to-many relationship between Collection and Product.
    # if a collection is deleted, all products in that collection will not be deleted.
    collection = models.ForeignKey(Collection, on_delete=models.PROTECT)
    # Each product can have many promotions, and each promotion can have many products.
    # The following field creates a many-to-many relationship between Promotion and Product.
    # you can add a key word argument "related_name" to the ManyToManyField to specify the name of the reverse relationship in the Promotion model. By default, Django will use the name of the model in lowercase, followed by _set. e.g products_set.
    # promotions = models.ManyToManyField(Promotion, related_name="products")
    promotions = models.ManyToManyField(Promotion, )
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['title']   
    
class Customer(models.Model):
    MEMBERSHIP_BRONZE = 'B'
    MEMBERSHIP_SILVER = 'S'
    MEMBERSHIP_GOLD = 'G'

    MEMBERSHIP_CHOICES = [
        (MEMBERSHIP_BRONZE, 'Bronze'),
        (MEMBERSHIP_SILVER, 'Silver'),
        (MEMBERSHIP_GOLD, 'Gold'),
    ]
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=255)
    birth_date = models.DateField(null=True)
    membership = models.CharField(
        max_length=1, choices=MEMBERSHIP_CHOICES, default=MEMBERSHIP_BRONZE)
    
    # order_set field will be created automatically because of it's relationship with Order table.
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    class Meta:
        ordering = ['first_name', 'last_name']

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
    
    
    # orderItem_set <--- cuz of the it's relationship with OrderItem
class OrderItem(models.Model):
    # If an order is deleted, OrderItem will not be deleted.
    # I.e, if order has at least one order item, the item will not be deleted.
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    # if we accidentally delete a product, we don't want to delete the order item.
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)

class Address(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    # the following field create one-to-one relationship between Customer and Address
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    
class Cart(models.Model):
    # this field will be autopopulated when a cart is created.
    created_at = models.DateTimeField(auto_now_add=True)


class CartItem(models.Model):
    # If a cart is deleted, CartItem will be also be deleted.
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    # if a product is deleted, CartItem will be also be deleted.
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()