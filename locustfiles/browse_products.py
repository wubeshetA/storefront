from random import randint
from locust import HttpUser, task, between

class WebsiteUser(HttpUser):
    wait_time = between(1, 5)  
    @task(2)
    def view_products(self):
        print("Viewing products...")
        collection_id = randint(3, 9)
        self.client.get(
            f'/store/products/?collection_id={collection_id}', 
            name='/store/products')
        
    @task(4)
    def view_product(self):
        print("Viewing a product...")
        product_id = randint(2, 900)
        self.client.get(f'/store/products/{product_id}/', 
                        name='/store/products/id')
    
    @task(1)
    def add_product_to_cart(self):
        print("Adding product to cart...")
        product_id = randint(2, 10)
        self.client.post(f'/store/carts/{self.cart_id}/items/',
                         name='/store/carts/items',
                         json={'product_id': product_id, 'quantity': 1},
                         )
        
    def on_start(self):
        # send a post request to the to cart endpoint and get id
        response = self.client.post('/store/carts/')
        result = response.json()
        self.cart_id = result['id']
