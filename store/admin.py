
from typing import Any
from django.contrib import admin
from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from . import models
from django.db.models.aggregates import Count
from django.utils.html import format_html, urlencode
from django.urls import reverse

# Register your models here.

class InventoryFilter(admin.SimpleListFilter):
    title = 'inventory'
    parameter_name = 'inventory'
    
    def lookups(self, request, model_admin):
        return [
            ('<10', 'Low'),
            ('>=10', 'OK')
        ]
    
    def queryset(self, request, queryset):
        if self.value() == '<10':
            return queryset.filter(inventory__lt=10)
        if self.value() == '>=10':
            return queryset.filter(inventory__gte=10)
@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    actions = ['clear_inventory']
    list_display = ('title', 'unit_price', 'collection', 'inventory_status')
    list_editable = ('unit_price',)
    list_per_page = 10
    
    list_filter = ('collection', 'last_update', InventoryFilter)
    
    @admin.display(ordering='inventory')
    def inventory_status(self, product):
        if product.inventory < 10:
            return 'Low'
        return 'OK'
    
    @admin.action(description='Clear inventory')
    def clear_inventory(self, request, queryset):
        """Custom action to clear the inventory of selected products.
        This action uses queryset.update() method to update multiple rows in the database
        without having to loop over them individually."""
        updated_count = queryset.update(inventory=0)
        self.message_user(request, f'{updated_count} products were successfully updated')

    
@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'membership', 'orders_count')
    list_editable = ('membership',)
    list_per_page = 10
    search_fields = ['first_name__istartswith', 'last_name__istartswith']
 
    
    @admin.display(ordering='orders_count')
    def orders_count(self, customer):
        # the following reverse method is used to get the url of the admin page we want to redirect to
        # here is the format of the reverse method
        # reverse(viewname, urlconf=None, args=None, kwargs=None, current_app=None)
        #  or 
        # reverse("admin:app_model_page") e.g reverse("admin:store_order_changelist")
        url = (
            reverse("admin:store_order_changelist")
                       + "?" 
                       + urlencode(
                           {"customer__id": str(customer.id)}
                           ))
        return format_html('<a href="{}">{}</a>', url, customer.orders_count)
    
    
    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
            return super().get_queryset(request).annotate(
                orders_count=Count('order')
            )
    


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
        # the following reverse method is used to get the url of the admin page we want to redirect to
        # here is the format of the reverse method
        # reverse(viewname, urlconf=None, args=None, kwargs=None, current_app=None)
        #  or 
        # reverse("admin:app_model_page")
        url = (
            reverse("admin:store_product_changelist")
                       + "?" 
                       + urlencode(
                           {"collection__id": str(collection.id)}
                           ))
        return format_html('<a href="{}">{}</a>', url, collection.products_count)
       
    
    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        return super().get_queryset(request).annotate(
            products_count=Count('product')
        )