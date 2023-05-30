from rest_framework import status
import pytest
from model_bakery import baker
from store.models import Collection

@pytest.fixture
def create_collection(api_client):
    def do_create_collection(collection):
        return api_client.post('/store/collections/', collection)
    return do_create_collection


@pytest.mark.django_db
class TestCreateCollection:
    def test_if_user_is_anonymous_returns_401(self, create_collection):
        # Arrange
        # Act
        response = create_collection({'title': 'a'})
        # Assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_admin_returns_403(self, authenticate, create_collection):

        authenticate(is_staff=False) # Arrage 
        response = create_collection({'title': 'a'}) # Act
        assert response.status_code == status.HTTP_403_FORBIDDEN # Assert

    def test_if_data_is_not_valid_returns_400(self, authenticate, create_collection):
        authenticate(is_staff=True)
        response = create_collection({'title': ''})
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data.get('title') is not None

    def test_if_data_is_valid_returns_201(self, authenticate, create_collection):

        authenticate(is_staff=True)
        response = create_collection({'title': 'a'})
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data.get('id') > 0
        
        

@pytest.mark.django_db
class TestRetrieveCollection:
    
    def test_if_collections_exist_returns_200(self, api_client):
        collection = baker.make(Collection)
        response = api_client.get(f'/store/collections/{collection.id}/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data == {
            'id': collection.id,
            'title': collection.title,
            'products_count': collection.products.count()
        }
        
    def test_if_collections_not_exist_returns_404(self, api_client):
        response = api_client.get(f'/store/collections/1/')
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_if_collection_has_products_returns_200(self, api_client):
        collection = baker.make(Collection)
        baker.make('store.Product', collection=collection, _quantity=3)
        response = api_client.get(f'/store/collections/{collection.id}/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data.get('products_count') == 3
        

@pytest.mark.django_db
class TestListCollection:
    
    def test_if_collections_exist_returns_200(self, api_client):
        baker.make(Collection, _quantity=3)
        response = api_client.get(f'/store/collections/')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 3
    
@pytest.mark.django_db
class TestUpdateCollection:
    def test_if_user_is_anonymous_returns_401(self, api_client):
        collection = baker.make(Collection)
        response = api_client.put(f'/store/collections/{collection.id}/', {'title': 'a'})
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_if_user_is_not_admin_returns_403(self, authenticate, api_client):
        collection = baker.make(Collection)
        authenticate(is_staff=False)
        response = api_client.put(f'/store/collections/{collection.id}/', {'title': 'a'})
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_if_data_is_not_valid_returns_400(self, authenticate, api_client):
        collection = baker.make(Collection)
        authenticate(is_staff=True)
        response = api_client.put(f'/store/collections/{collection.id}/', {'title': ''})
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data.get('title') is not None
    
    def test_if_collection_not_exist_returns_404(self, authenticate, api_client):
        authenticate(is_staff=True)
        response = api_client.put(f'/store/collections/1/', {'title': 'a'})
        assert response.status_code == status.HTTP_404_NOT_FOUND
        
    def test_if_data_is_valid_returns_200(self, authenticate, api_client):
        collection = baker.make(Collection)
        authenticate(is_staff=True)
        response = api_client.put(f'/store/collections/{collection.id}/', {'title': 'a'})
        assert response.status_code == status.HTTP_200_OK
        assert response.data.get('title') == 'a'
        
@pytest.mark.django_db
class TestDeleteCollection:
    
    def test_if_user_is_anonymous_returns_401(self, api_client):
        collection = baker.make(Collection)
        response = api_client.delete(f'/store/collections/{collection.id}/')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_if_user_is_not_admin_returns_403(self, authenticate, api_client):
        collection = baker.make(Collection)
        authenticate(is_staff=False)
        response = api_client.delete(f'/store/collections/{collection.id}/')
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_if_collection_not_exist_returns_404(self, authenticate, api_client):
        authenticate(is_staff=True)
        response = api_client.delete(f'/store/collections/1/')
        assert response.status_code == status.HTTP_404_NOT_FOUND
        
    def test_if_collection_exist_returns_204(self, authenticate, api_client):
        collection = baker.make(Collection)
        authenticate(is_staff=True)
        response = api_client.delete(f'/store/collections/{collection.id}/')
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert response.data is None
        

    