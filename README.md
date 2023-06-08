# Store Front - Django Online Store Backend

This a backend for an ecommerce application built with Django framework and Django Rest framework.
It provides the necessary APIs and database models to manage an online store.
The project includes a Django app called "store" which contains the core models for the ecommerce functionality.
Additionally, there are decoupled apps, namely "likes" and "tags", that can be used separately in other projects.
The "core" app acts as a communication hub between these apps and also includes a custom user model for user management.

## Features

Among with many other features the project includes the following core functionalities:

- User/Customer Authentication and Authorizations for accessing their data (such as orders, cart items, etc.)
- Admin panel for managing the store (products, orders, customers, etc.) for admin users
- Handle the appropriate CRUD operations for products, orders, product catergories, reviews, etc.
- Supports search and filtering capabilities to help customers and admins find products based on specific criteria

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
    On Unix/Linux: 
    ```sh
    pipenv shell
    ```
5. Install the required dependencies (This depencendencies are listed in the Pipfile):
    ```sh
    pipenv install
    ```
6. Update the development settings in [./storefront/settings/dev.py](./storefront/settings/dev.py) file based on your local development configuration cessary database

7. Apply the database migrations:
    ```sh
    python manage.py migrate
    ```
8. Start the development server:
    ```sh
    python manage.py runserver
    ```
    You can now access the Django backend at http://localhost:8000/
9. Optional for VSCode user - If you are using VSCode as your IDE, you can select the virtual environment
    you just created as your python interpreter. This will enable you to use the virtual
    environment in your IDE. To do this, open the command palette (Ctrl+Shift+P) and type
    "Python: Select Interpreter" and select the virtual environment you just created.
    To see the path to the virtual environment, run the following command in the terminal and have a look at the path displayed.
    ```sh
    pipenv --venv
    ```
