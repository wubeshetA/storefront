from django.shortcuts import get_object_or_404
# import Count class
from django.db.models import Count
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
# from rest_framework import mixins
# import GenericAPIView 
from rest_framework.generics import (ListCreateAPIView, 
                                     RetrieveUpdateDestroyAPIView)
from .models import Collection, Product
from .serializer import ProductSerializer
from .serializer import CollectionSerializer

#================ Views For Product ================= 



    
class ProductList(ListCreateAPIView):
    
    queryset = Product.objects.select_related('collection').all()
    
    def get_serializer_class(self):
        return ProductSerializer
    
    def get_serializer_context(self):
         return {'request': self.request}
    # if queryset attribute is defined, no need to define get_queryset method
    # def get_queryset(self):
    #     return Product.objects.select_related('collection').all()



# The following commented code is the same as the above code, but it is
# but it used APIView from rest_framework.views, however, the above code
# uses generics

# class ProductList(APIView):
    
#     def get(self, request, *args, **kwargs):
#         products = Product.objects.select_related('collection').all()
#         serializer = ProductSerializer(products, many=True, context={'request': request})
#         return Response(serializer.data)
    
#     def post(self, request, *args, **kwargs):
#         serializer = ProductSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
    

# class ProductDetail(RetrieveUpdateDestroyAPIView):
    
#     # queryset = get_object_or_404(Product, pk=id)
#     lookup_field = 'id'
#     def get_queryset(self):
#          return get_object_or_404(Product, pk=self.kwargs.get('id'))
     
#     def get_serializer_class(self):
#         return ProductSerializer


# =======products details
# class ProductDetail(APIView):
    
#     def product(self, id):
#         return get_object_or_404(Product, pk=id)
    
#     def get(self, request, id):
#         serializer = ProductSerializer(self.product(id))
#         return Response(serializer.data)
    
#     def put(self, request, id):
#         serializer = ProductSerializer(self.product(id), data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    
#     def delete(self, request, id):
#         self.product(id).delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
    
# recreate the above views using GenericAPIView and mixins
class ProductDetail(RetrieveUpdateDestroyAPIView):
    
    # queryset = Product.objects.all()
    # lookup_field = 'id'
    
    # we can use the above 2 lines of or the following line of code
    def get_object(self):
         return get_object_or_404(Product, pk=self.kwargs.get('id'))
    
    serializer_class = ProductSerializer
    

"""The following commented code is the same as the above code, but it is 
written as a function-based view instead of a class-based view.
"""

# @api_view(["GET", "POST"])
# def products_list(request):
#     if request.method == "GET":
#         pass
    
#     elif request.method == "POST":
#         pass

# @api_view(["GET", "PUT", "DELETE"])
# def product_detail(request, id):
    
#     product = get_object_or_404(Product, pk=id)
#     if request.method == "GET":
#         pass
    
#     elif request.method == "PUT":
#         serializer = ProductSerializer(product, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    
#     elif request.method == "DELETE":
#         product.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


#============================= VIEW FOR COLLECTIONS ========================= 


class CollectionList(ListCreateAPIView):
    queryset = Collection.objects.annotate(products_count=Count('products')).all()
    
    def get_serializer_class(self):
        return CollectionSerializer
    
# ==================== The following is a APIView class view for CollectionList
# The above code is a generic view for CollectionList


# class CollectionList(APIView):
        
#         def get(self, request, *args, **kwargs):
#             queryset = Collection.objects.annotate(products_count=Count('products')).all()
#             serializer = CollectionSerializer(queryset, many=True)
#             return Response(serializer.data)
        
#         def post(self, request, *args, **kwargs):
#             serializer = CollectionSerializer(data=request.data)
#             serializer.is_valid(raise_exception=True)
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)


"""The following commented code is the same as the above code, but it is
written as a function-based view instead of a class-based view."""

# @api_view(['GET', 'POST'])
# def collections_list(request):
#     if request.method == "GET":
#         queryset = Collection.objects.annotate(products_count=Count('product')).all()
#         serializer = CollectionSerializer(queryset, many=True)
#         return Response(serializer.data)
    
#     elif request.method == "POST":
#         serializer = CollectionSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)

class CollectionDetail(APIView):
            
            def collection(self, id):
                return get_object_or_404(
                    Collection.objects.annotate(products_count=Count('products')).all(),
                    pk=id)
            
            def get(self, request, id):
                serializer = CollectionSerializer(self.collection(id))
                return Response(serializer.data)
            
            def put(self, request, id):
                serializer = CollectionSerializer(self.collection(id), data=request.data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
            
            def delete(self, request, id):
                if self.collection(id).products.count() > 0:
                    return Response(
                        {'error': 'You cannot delete a collection that has products.'},
                        status=status.HTTP_405_METHOD_NOT_ALLOWED
                    )
                self.collection(id).delete()
                return Response(status=status.HTTP_204_NO_CONTENT)

"""The following commented code is the same as the above code, but it is
written as a function-based view instead of a class-based view."""

# @api_view(['GET', 'PUT', 'DELETE'])
# def collection_detail(request, pk):
#     collection = get_object_or_404(
#         Collection.objects.annotate(products_count=Count('products')).all(),
#         pk=pk)
    
#     if request.method == "GET":
#         serializer = CollectionSerializer(collection)
#         return Response(serializer.data)
    
#     elif request.method == "PUT":
#         serializer = CollectionSerializer(collection, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    
#     elif request.method == "DELETE":
#         if collection.products.count() > 0:
#             return Response(
#                 {'error': 'You cannot delete a collection that has products.'},
#                 status=status.HTTP_405_METHOD_NOT_ALLOWED
#             )
#         collection.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
