from django.shortcuts import render
from django.http import HttpResponse
import requests
from store.models import Product
from store.models import Customer
from store.models import Collection
from store.models import Order
from store.models import OrderItem
from django.core.cache import cache
from django.db.models import Q, F

from django.db.models.aggregates import Count, Sum, Max, Min, Avg
# import ExpressionWrapper
from django.db.models.expressions import ExpressionWrapper
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.core.mail import EmailMessage, BadHeaderError, send_mail
from rest_framework.views import APIView
from .tasks import notify_customers
# Create your views here.
# def hello_world(request):
    
#     key = "httpbin_response"
#     if cache.get(key) is None:
#         response = requests.get('https://httpbin.org/delay/2')
#         data = response.json()
#         cache.set(key, data)
#     # send request to the api that repond after some delay
#     # response = requests.get('https://httpbin.org/delay/2')
#     return HttpResponse(cache.get(key))


class ViewHello(APIView):
    
    @method_decorator(cache_page(60))
    def get(self, request):
        response = requests.get('https://httpbin.org/delay/2')
        data = response.json()
        return HttpResponse(data)
    
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
    # queryset = Product.objects.filter(inventory__lt=10, unit_price__lt=20)
    
    # Products: inventory < 10 OR price < 20
    # queryset = Product.objects.filter(Q(inventory__lt=10) | Q(unit_price__lt=20))
    
    # Select products that have been ordered and sort them by title
    
    # queryset = OrderItem.objects.values('product_id')
    
    
    
    # queryset = Product.objects.filter(inventory = F('unit_price'))
    # for product in queryset:
    #     print("=======")
    #     print(product.inventory, product.unit_price)
    
    #!: Exerices on Aggregate
    
    # How many orders do we have?
    # ======== solutions =============
    # queryset = Order.objects.aggregate(count=Count("id"))
    # print(queryset)
    
    # •How many units of product 1 have we sold?
    # queryset = OrderItem.objects.filter(product_id=1).aggregate(quantity_sold=Sum("quantity"))
    # print(queryset)
    # •How many orders has customer 1 placed?
    # queryset = Order.objects.filter(customer__id=1).aggregate(customer_orders=Count("*"))
    # print(queryset)
    # •What is the min, max and average price of the products in collection 3?
    # queryset = Product.objects.filter(collection__id=3).aggregate(min = Min('unit_price'), max = Max('unit_price'), average=Avg('unit_price'))
    # print(queryset)
    
    
    
    #!: Exerices on Anotation
    
    # •Customers with their last order ID
    # queryset = Customer.objects.annotate(last_order_id=Max('order__id'))

    # •Collections and count of their products
    # queryset = Collection.objects.annotate(number_of_products=Count('product'))
    # •Customers with more than 5 orders 

    # queryset = Customer.objects.annotate(frequent_customers=Count('order')).filter(frequent_customers__gt=5)
    # print(queryset)
    
    # •Customers and the total amount they’ve spent
    # queryset = Customer.objects.annotate(
    #     total_spent=Sum(F('order__orderitem__quantity') * F('order__orderitem__unit_price'))
        # )
    # print(queryset)
    
    #•Top 5 best-selling products and their total sales
    # queryset = Product.objects.annotate(
    #     total_sales=Sum(F('orderitem__quantity') * F('orderitem__unit_price'))
    # ).order_by('-total_sales')[:5]
    # print(queryset)
    
    # * sending emails
    # try:
    #     message = EmailMessage('Subject', 'body message', 'fromwube@info.com', ['wubesehttt@gmail.com'])
    #     message.attach_file('playground/static/images/cat.jpeg')
    #     message.send()
    #     print('message sent successfully')
    #     # send_mail('subject', 'message', 'info@wube.com', ['w.yimam@alustudent.com'])
    # except BadHeaderError:
    #     return HttpResponse('Invalid header found.')
    # return HttpResponse('Success')
    
    # send mail
    
    
    
    # return render(request, 'hello.html', {'name': 'Wube'})