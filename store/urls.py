from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.ProductList.as_view()),
    path('products/<int:id>/', views.ProductDetail.as_view()),
    
    # on the following path, the <int:pk> is the primary key of the collection.
    # django uses pk to identify the primary key of the model.
    # you should not use id in the path, because it is not the primary key of the model.
    path('collections/', views.CollectionList.as_view()),
    path('collections/<int:pk>/', views.CollectionDetail.as_view(), name='collection-detail'),
]