from django.shortcuts import get_object_or_404
# import Count class
from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.mixins import (CreateModelMixin,
                                   RetrieveModelMixin, 
                                   DestroyModelMixin)

# from rest_framework import mixins
# import GenericAPIView
from rest_framework.generics import (ListCreateAPIView, 
                                     RetrieveUpdateDestroyAPIView,
                                     )
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from .pagination import ProductPagination
from .filters import ProductFilter
from .models import Cart, CartItem, Collection, OrderItem, Product, Review
from .serializer import AddCartItemSerializer, CartItemSerializer, CartSerializer, ProductSerializer, ReviewSerializer, UpdateCartItemSerializer
from .serializer import CollectionSerializer


################### Views For Product ##########################

""" ============== Product view using ViewSet ================== """
class ProductViewSet(ModelViewSet):
    """ ModelViewSet for Product
    """
    # * if we want only a readonly operation, we can use ReadOnlyModelViewSet
    # * if we want only a create operation, we can use CreateModelViewSet
    queryset = Product.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    # filterset_fields = ['collection_id']
    filterset_class = ProductFilter
    # add searching for title and description
    search_fields = ['title', 'description']
    ordering_fields = ['unit_price', 'last_update']
    # set pagination
    pagination_class = ProductPagination
    
    # The following queryset is used to filter the products based on the
    # collection_id. The collection_id is passed as a query parameter.
    # However, currently we are using DjangoFilterBackend to filter the
    # so we don't need to have this functionality
    # def get_queryset(self):
    #     queryset = Product.objects.all()
    #     collection_id = self.request.query_params.get('collection_id')
    #     if collection_id is not None:
    #         queryset = queryset.filter(collection_id=collection_id)
    #     return queryset
    
    serializer_class = ProductSerializer
    def get_serializer_context(self):
        return {'request': self.request}
    
    def destroy(self, request, *args, **kwargs):
        
        # ? Come back to this later
        if OrderItem.objects.filter(product_id=kwargs['pk']).exists():
            return Response({'message': 'This product cannot be deleted because it has already been ordered.'},
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)
    


""" ============ GenericView based Product view ================= """ 
# class ProductList(ListCreateAPIView):
    
    # queryset = Product.objects.select_related('collection').all()
    
    # def get_serializer_class(self):
    #     return ProductSerializer
    
    # def get_serializer_context(self):
    #      return {'request': self.request}
     
    # def delete(self, request, pk):
    #     product = get_object_or_404(Product, pk=pk)
    #     if product.orderitems.count() > 0:
    #         return Response({'message': 'This product cannot be deleted because \
    #                          it has already been ordered.'},
    #                         status=status.HTTP_405_METHOD_NOT_ALLOWED)
    #     product.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)
    
    
    
# class ProductDetail(RetrieveUpdateDestroyAPIView):
    
#     # def get_object(self):
#     #      return get_object_or_404(Product, pk=self.kwargs.get('pk'))
#     # we can use the above 2 lines of or the following line of code
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
    
#     def delete(self, request, pk):
#         product = get_object_or_404(Product, pk=pk)
#         if product.orderitems.count() > 0:
#             return Response({'message': 'This product cannot be deleted because it has already been ordered.'},
#                             status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         product.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


    # if queryset attribute is defined, no need to define get_queryset method
    # def get_queryset(self):
    #     return Product.objects.select_related('collection').all()

"""====================== Product using mixins ======================="""


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


""" ================ Product view by function view =============================""" 

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


######################### VIEW FOR COLLECTIONS ############################ 

""" ================= Collection views using ViewSet ================== """
class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.annotate(products_count=Count('products')).all()
    serializer_class = CollectionSerializer
    
    def destroy(self, request, pk):
            collection = get_object_or_404(Collection, pk=pk)
            if collection.products.count() > 0:
                return Response(
                    {'error': 'You cannot delete a collection that has products.'},
                    status=status.HTTP_405_METHOD_NOT_ALLOWED
                )
            collection.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    
    
""" ================= Collection views using generics ================== """
class CollectionList(ListCreateAPIView):
    queryset = Collection.objects.annotate(products_count=Count('products')).all()
    
    def get_serializer_class(self):
        return CollectionSerializer


# convert the above view to a generic view using GenericAPIView and mixins
class CollectionDetail(RetrieveUpdateDestroyAPIView):
        
        queryset = Collection.objects.annotate(products_count=Count('products')).all()
        
        # We can the following line of code as alternative to the above line of code
        # def get_object(self):
        #     return get_object_or_404(
        #         Collection.objects.annotate(products_count=Count('products')).all(),
        #         pk=self.kwargs.get('pk'))
        
        serializer_class = CollectionSerializer
        # override the destroy method to check if the collection has products
        def delete(self, request, pk):
            collection = get_object_or_404(Collection, pk=pk)
            if collection.products.count() > 0:
                return Response(
                    {'error': 'You cannot delete a collection that has products.'},
                    status=status.HTTP_405_METHOD_NOT_ALLOWED
                )
            collection.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


    
# ==================== The following is a APIView class view for CollectionList
# The above code is a generic view for CollectionList

""" ====================== Collection view using mixins ================== """

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
# class CollectionDetail(APIView):
            
#             def collection(self, id):
#                 return get_object_or_404(
#                     Collection.objects.annotate(products_count=Count('products')).all(),
#                     pk=id)
            
#             def get(self, request, id):
#                 serializer = CollectionSerializer(self.collection(id))
#                 return Response(serializer.data)
            
#             def put(self, request, id):
#                 serializer = CollectionSerializer(self.collection(id), data=request.data)
#                 serializer.is_valid(raise_exception=True)
#                 serializer.save()
#                 return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
            
#             def delete(self, request, id):
#                 if self.collection(id).products.count() > 0:
#                     return Response(
#                         {'error': 'You cannot delete a collection that has products.'},
#                         status=status.HTTP_405_METHOD_NOT_ALLOWED
#                     )
#                 self.collection(id).delete()
#                 return Response(status=status.HTTP_204_NO_CONTENT)


""" =========== function-based Collection view using  ============= """


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

class ReviewViewSet(ModelViewSet):
    # queryset = Review.objects.all()
    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs.get('product_pk'))
    #! use context object to pass additional information to the serializer
    def get_serializer_context(self):
        return {'product_id': self.kwargs.get('product_pk')}
    serializer_class = ReviewSerializer
    
    
class CartViewSet(CreateModelMixin,
                  RetrieveModelMixin,
                  DestroyModelMixin,
                  GenericViewSet):
    queryset = Cart.objects.prefetch_related('items__product').all()
    serializer_class = CartSerializer

class CartItemViewSet(ModelViewSet):
    
    http_method_names = ['get', 'post', 'patch', 'delete']
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddCartItemSerializer
        elif self.request.method == 'PATCH':
            return UpdateCartItemSerializer
        return CartItemSerializer
    
    def get_queryset(self):
        return CartItem.objects.filter(cart_id=self.kwargs.get('cart_pk'))\
            .select_related('product')
    
    def get_serializer_context(self):
        return {'cart_id': self.kwargs.get('cart_pk')}
    

