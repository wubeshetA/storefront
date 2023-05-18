from django.shortcuts import get_object_or_404
# import Count class
from django.db.models import Count
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Collection, Product
from .serializer import ProductSerializer
from .serializer import CollectionSerializer


#================ Views For Product ================= 

@api_view(["GET", "POST"])
def products_list(request):
    if request.method == "GET":
        products = Product.objects.select_related('collection').all()
        serializer = ProductSerializer(products, many=True, context={'request': request})
        return Response(serializer.data)
    
    elif request.method == "POST":
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(["GET", "PUT", "DELETE"])
def product_detail(request, id):
    
    product = get_object_or_404(Product, pk=id)
    if request.method == "GET":
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    
    elif request.method == "PUT":
        serializer = ProductSerializer(product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    
    elif request.method == "DELETE":
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

#================ Views For Collection ================= 

@api_view(['GET', 'POST'])
def collections_list(request):
    if request.method == "GET":
        queryset = Collection.objects.annotate(products_count=Count('product')).all()
        serializer = CollectionSerializer(queryset, many=True)
        return Response(serializer.data)
    
    elif request.method == "POST":
        serializer = CollectionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET', 'PUT', 'DELETE'])
def collection_detail(request, pk):
    collection = get_object_or_404(Collection, pk=pk)
    
    if request.method == "GET":
        serializer = CollectionSerializer(collection)
        return Response(serializer.data)
    
    elif request.method == "PUT":
        serializer = CollectionSerializer(collection, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    
    elif request.method == "DELETE":
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
