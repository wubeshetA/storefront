from django.shortcuts import render
from django.http import HttpResponse
from store.models import Product
from store.models import Customer
from store.models import Collection
from store.models import Order
from store.models import OrderItem
from django.db.models import Q, F
# Create your views here.
def hello_world(request):
    
    # query_set = Product.objects.all()
    # for item in query_set:
    #     # print(item)
    #     pass
    # =================================
    # exercise 1
    # customers = Customer.objects.filter(email__endswith=".com")
    # for customer in customers:
    #     print(customer, " " ,customer.email)
        
    # ==========================================
    # exercise 2
    # collections = Collection.objects.filter(featured_product__isnull=True)
    # for collection in collections:
    #     print(collection, " " ,collection.featured_product)
    
    # =================================================
    # exercise 3
    # products = Product.objects.filter(inventory__lt=10)
    # for product in products:
    #     print(product.title, " " ,product.inventory)
    
    # =========================================
    # exercise 4
    # orders = Order.objects.filter(customer=6)
    # for order in orders:
    #     print(order.id, " " ,order.customer)
    # =====================================================
    
    # exercise 5
    # query_set = Product.objects.all()
    # order_items = OrderItem.objects.filter(product__collection__id=3)
    # for item in order_items:
    #     print(item.id, " " ,item.product.title, item.product.collection.pk, item.product.collection.title)
    
    
    # ================== Using Q objects =================
    
    # Products: inventory < 10 AND price < 20
    queryset = Product.objects.filter(inventory__lt=10, unit_price__lt=20)
    
    # Products: inventory < 10 OR price < 20
    queryset = Product.objects.filter(Q(inventory__lt=10) | Q(unit_price__lt=20))
    
    
    
    
    
    return render(request, 'hello.html', {'name': 'Wube'})