import pytest
from rest_framework import status
from model_bakery import baker
# import APIclient
from rest_framework.test import APIClient
from django.contrib.auth.models import User

from store.models import Collection, Product
@pytest.fixture
def create_product(api_client):
    def do_create_product(product):
        return api_client.post('/store/products/', product)
    return do_create_product


# @pytest.fixture
# def update_product(api_client):
#     def do_update_product(product):
#         return api_client.put('/store/products/', product)
#     return do_update_product

@pytest.mark.django_db
class TestCreateProduct:
    
    def test_if_user_is_anonymous_returns_401(self, create_product):
        response = create_product({})
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_if_user_is_not_admin_returns_403(self, authenticate, create_product):
        authenticate(is_staff=False)
        response = create_product({})
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_if_data_is_not_valid_returns_400(self, authenticate, create_product):
        authenticate(is_staff=True)
        response = create_product(
                {
                    "Title": "a",
                    "Description": "b",
                    "Unit price": 1,
                    "Inventory": 1,
                    # "Collection": 1 # Collection missing
                }
            )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        
    def test_if_data_is_valid_returns_201(self, authenticate, create_product):
        authenticate(is_staff=True)
        collection = baker.make(Collection)
        response = create_product(
            {
                "title": "a",
                "description": "description",
                "unit_price": 5,
                "inventory": 2,
                "collection": collection.id
            }
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data.get('id') > 0

@pytest.mark.django_db
class TestUpdateProduct:
    def test_if_user_is_anonymous_returns_401(self):
        client = APIClient()
        response = client.put('/store/products/1/', {})
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_if_user_is_not_admin_returns_403(self, api_client, authenticate):

        authenticate(is_staff=False)
        response = api_client.put('/store/products/1/', {})
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_if_product_not_exit_return_404(self, api_client, authenticate):
        authenticate(is_staff=True)
        response = api_client.put('/store/products/1/', {})
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_if_data_is_not_valid_returns_400(self, api_client, authenticate):
        authenticate(is_staff=True)
        baker.make(Product, id=1)
        response = api_client.put('/store/products/1/', {}) # empty data
        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    def test_if_data_is_valid_returns_200(self, api_client, authenticate):
        authenticate(is_staff=True)
        product = baker.make(Product, id=1)
        print("=====================================")
        print(product.__dict__)
        response = api_client.put(f'/store/products/{product.id}/', {
            "title": product.title,
            "description": "updated description",
            "unit_price": 4,
            "inventory": 2,
            "collection": product.collection.id
        })
        assert response.status_code == status.HTTP_200_OK
        assert response.data.get('id') == product.id
        assert response.data.get('description') == "updated description"


@pytest.mark.django_db
class TestDeleteProduct:
    
    def test_if_user_is_anonymous_returns_401(self, api_client):
        response = api_client.delete('/store/products/1/')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_if_user_is_not_admin_returns_403(self, api_client, authenticate):
        authenticate(is_staff=False)
        response = api_client.delete('/store/products/1/')
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_if_product_not_exit_return_404(self, api_client, authenticate):
        authenticate(is_staff=True)
        response = api_client.delete('/store/products/1/')
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_if_product_exists_returns_204(self, api_client, authenticate):
        authenticate(is_staff=True)
        product = baker.make(Product, id=1)
        response = api_client.delete(f'/store/products/{product.id}/')
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert response.data is None
    
@pytest.mark.django_db
class TestGetProduct:
    pass