# Store Front - Django Online Store Backend

This is a backend for an ecommerce application built with Django and Django Rest framework.
It provides the necessary RESTful APIs and database models to manage an online store.
The project includes a Django app called "store" which contains the core models for the ecommerce functionality.
Additionally, there are decoupled apps, namely "likes" and "tags", that can be used separately in other projects.
The "core" app acts as a communication hub between these apps and also includes a custom user model for user management.

## Features

Among with many other features the project includes the following core functionalities:

- User/Customer Authentication and Authorizations for accessing their data (such as orders, cart items, etc.)
- Admin panel for managing the store (products, orders, customers, etc.) for admin users
- Handle the appropriate CRUD operations for products, orders, product catergories, reviews, etc.
- Supports search and filtering capabilities to help customers and admins find products based on specific criteria
- Exposes a RESTful API with exhaustive documentation for the above functionalities

## Requirements
 - Python 3.11 or higher

## Installation and Setup
To set up this Django backend project locally, follow these steps:

1. Clone the repository
    ```sh
    git clone https://github.com/wubeshetA/storefront.git
    ```

2. Change into the project directory
    ```sh
    cd storefront
    ```
3. Install pipenv dependecy management tool with the following command. This project
uses pipenv to create isolated virtual environement and manage third party packages.
    ```sh
    pip install pipenv
    ```
4. Activate the virtual environment:
    ```sh
    pipenv shell
    ```
5. Install the required dependencies (This depencendencies are listed in the Pipfile):
    ```sh
    pipenv install
    ```
6. Update the development settings at [./storefront/settings/dev.py](./storefront/settings/dev.py) file based on your local development configuration cessary database

7. Apply the database migrations:
    ```sh
    python manage.py migrate
    ```
8. Start the development server:
    ```sh
    python manage.py runserver
    ```
    You can now access the Django backend at http://localhost:8000/
9. If you want to seed the database with some sample data, run the following command:
    ```sh
    python manage.py seed_db
    ```
10. Optional for VSCode user - If you are using VSCode as your IDE, you can select the virtual environment
    you just created as your python interpreter. This will enable you to use the virtual
    environment in your IDE. To do this, open the command palette (Ctrl+Shift+P) and type
    "Python: Select Interpreter" and select the virtual environment you just created.
    To see the path to the virtual environment, run the following command in the terminal and have a look at the path displayed.
    ```sh
    pipenv --venv
    ```

## Testing
All the tests for this project are located in the [./store/tests](./store/tests) directory.
To run all the tests at once, run the following command from the root directory:
```sh
pytest
```

## API Reference

Full API documentation is available at [http://localhost:8000/docs/](http://localhost:8000/docs/)

### Key Models in the "store" App
The "store" app includes the following important models (database tables):

- Promotion: Represents promotional offers or discounts.
- Collection: Represents a curated collection of products.
- Product: Represents a product available for sale.
- ProductImage: Represents images associated with a product.-. 
- Customer: Represents a customer or user of the ecommerce platform.
- Order: Represents an order placed by a customer.
- OrderItem: Represents an individual item within an order.
- Address: Represents a shipping or billing address for a customer.
- Cart: Represents a shopping cart for a customer.
- CartItem: Represents an item within a shopping cart.
- Review: Represents a customer's review or rating for a product.

## Deployment

This project is deployed on Digital Ocean. You can access it at [https://storefront-nsnsl.ondigitalocean.app/](https://storefront-nsnsl.ondigitalocean.app/)

## Author

👤 [**Wubeshet Yimam**](https://github.com/wubeshetA)