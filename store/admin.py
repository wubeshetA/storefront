
from typing import Any
from django.contrib import admin
from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from . import models
from django.db.models.aggregates import Count
from django.utils.html import format_html

# Register your models here.

@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'unit_price', 'inventory_status')
    list_editable = ('unit_price',)
    list_per_page = 10
    
    @admin.display(ordering='inventory')
    def inventory_status(self, product):
        if product.inventory < 10:
            return 'Low'
        return 'OK'
    
@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'membership')
    list_editable = ('membership',)
    list_per_page = 10


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'placed_at', 'customer')
    list_per_page = 10
    # list_select_related attribute is used to optimize the query by pre-fetching the related objects

    
@admin.register(models.Collection)

class CollectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'products_count')
    
    @admin.display(ordering='products_count')
    def products_count(self, collection):
        return collection.products_count
    
    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        return super().get_queryset(request).annotate(
            products_count=Count('product')
        )