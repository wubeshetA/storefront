from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.products_list),
    path('products/<int:id>/', views.product_detail),
    
    # on the following path, the <int:pk> is the primary key of the collection.
    # django uses pk to identify the primary key of the model.
    # you should not use id in the path, because it is not the primary key of the model.
    path('collections/<int:pk>/', views.collections_list, name='collection-detail'),
]