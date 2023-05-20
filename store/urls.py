from django.urls import include, path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('products', views.ProductViewSet)
router.register('collections', views.CollectionViewSet)

urlpatterns = router.urls
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