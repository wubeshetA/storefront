from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Collection, Product
from .serializer import ProductSerializer


# @api_view()
# def collections_list(request):
#     collections = Product.objects.all()
#     return Response(collections)

@api_view()
def products_list(request):

    products = Product.objects.select_related('collection').all()
    serializer = ProductSerializer(products, many=True, context={'request': request})
    return Response(serializer.data)

@api_view()
def product_detail(request, id):
    product = get_object_or_404(Product, pk=id)
    serializer = ProductSerializer(product)
    return Response(serializer.data)

@api_view()
def collections_list(request, pk):
    collections = Collection.objects.all()
    serializer = ProductSerializer(collections, many=True)
    return Response({'collections': 'ok'})
# Create your views here.
