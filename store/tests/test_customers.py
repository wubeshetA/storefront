from rest_framework import status
import pytest

@pytest.mark.django_db
class TestListCustomer:
    
    def test_if_user_is_anonymous_returns_401(self, api_client):
        response = api_client.get('/store/customers/')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_if_user_is_not_admin_returns_403(self, authenticate, api_client):
        authenticate(is_staff=False)
        response = api_client.get('/store/customers/')
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_if_user_is_admin_returns_200(self, authenticate, api_client):
        authenticate(is_staff=True)
        response = api_client.get('/store/customers/')
        assert response.status_code == status.HTTP_200_OK

@pytest.mark.django_db
class TestGetCustomerProfile:
    
    def test_if_user_is_anonymous_returns_401(self, api_client):
        response = api_client.get('/store/customers/me/')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        
    # def test_if_user_is_authenticated_returns_200(self, api_client, authenticate):
    #     authenticate(is_staff=False)
    #     user = baker.make()
    #     customer = baker.make(Customer, user_id=user.id)
    #     response = api_client.get('/store/customers/me/')
    #     assert response.status_code == status.HTTP_200_OK
        
@pytest.mark.django_db
class TestUpdateCustomerProfile:
    
    def test_if_user_is_anonymous_returns_401(self, api_client):
        response = api_client.put('/store/customers/me/')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        
    # def test_if_user_is_authenticated_returns_200(self, authenticate, api_client):
    #     authenticate()
    #     # create a user to get it's id
    #     user = baker.make(User)
    
        
        
        
