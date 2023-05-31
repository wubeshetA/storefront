from django.urls import path
from . import views

urlpatterns = [
    path('hello/', views.ViewHello.as_view(), name='hello'),
]