from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()
router.register(r'products', views.ProductViewSet, basename='product')
router.register(r'collections', views.CollectionViewSet)
router.register(r'carts', views.CartViewSet, basename='cart')
router.register(r'customers', views.CustomerViewSet, basename='customer')
router.register(r'orders', views.OrderViewSet, basename='order')

reviews_router = routers.NestedSimpleRouter(router, r'products', lookup='product')
reviews_router.register(r'reviews', views.ReviewViewSet, basename='product-reviews')

cart_items_router = routers.NestedSimpleRouter(router, r'carts', lookup='cart')
cart_items_router.register(r'items', views.CartItemViewSet, basename='cart-items')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(reviews_router.urls)),
    path('', include(cart_items_router.urls)),
]

# if there is a custome path, you can use the following code:
# urlpatterns = [
#     path('', include(router.urls)),
#     path('')
# ]

# The following urlpatterns are replaced by the above as we are using
# viewsets and routers.

# urlpatterns = [
#     path('products/', views.ProductList.as_view()),
#     path('products/<int:pk>/', views.ProductDetail.as_view()),
    
#     # on the following path, the <int:pk> is the primary key of the collection.
#     # django uses pk to identify the primary key of the model.
#     # you should not use id in the path, because it is not the primary key of the model.
#     path('collections/', views.CollectionList.as_view()),
#     path('collections/<int:pk>/', views.CollectionDetail.as_view(), name='collection-detail'),
# ]