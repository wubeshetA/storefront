import pytest
from rest_framework import status
from model_bakery import baker

from store.models import Collection
@pytest.fixture
def create_product(api_client):
    def do_create_product(product):
        return api_client.post('/store/products/', product)
    return do_create_product

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
         
class TestUpdateProduct:
    pass
class TestDeleteProduct:
    pass
class TestGetProduct:
    pass