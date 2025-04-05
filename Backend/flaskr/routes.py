from urllib import response
from flask import Blueprint, request, jsonify, redirect, url_for
from flasgger import swag_from
from .database import db
from .datamodels import *
from .request_handling import contracts_service, customers_service, auth_service, users_service, wares_service
from .auth.validate_request import validate_admin_request

# Blueprints
users_bp = Blueprint('users', __name__, url_prefix='/api')
customers_bp = Blueprint('customers', __name__, url_prefix='/api')
contracts_bp = Blueprint('contracts', __name__, url_prefix='/api')
wares_bp = Blueprint('wares', __name__, url_prefix='/api')
auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

### Authentication ###
@auth_bp.route("/login", methods=['POST'])
@swag_from({
    'tags': ['Login'],
    'summary': 'User Login',
    'description': 'Authenticate user and return a session token.',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'username': {'type': 'string'},
                    'password': {'type': 'string'}
                }
            }
        }
    ],
    'responses': {
        200: {'description': 'Successful login'},
        401: {'description': 'Unauthorized'}
    }
})
def user_login():
    return auth_service.handle_login_request(request)

### User ###
@users_bp.route('/users', methods=['POST'])
@swag_from({
    'tags': ['User'],
    'summary': 'Create a User',
    'description': 'Creates a new user with the given details.',
    'responses': {
        201: {'description': 'User created successfully'},
        400: {'description': 'Bad request'}
    }
})
def create_user():
    res = validate_admin_request(request)
    if res:
        return res
    return users_service.create_user(request)

@users_bp.route('/users', methods=['GET'])
@swag_from({
    'tags': ['User'],
    'summary': 'Get Users',
    'description': 'Retrieves all users from the system.',
    'responses': {
        200: {'description': 'A list of users'}
    }
})
def get_users():
    return users_service.get_users(request)

@users_bp.route('/users/<int:user_id>', methods=['GET'])
@swag_from({
    'tags': ['User'],
    'summary': 'Get User by ID',
    'description': 'Retrieve details of a specific user.',
    'parameters': [{
        'name': 'user_id',
        'in': 'path',
        'required': True,
        'type': 'integer'
    }],
    'responses': {
        200: {'description': 'User details'},
        404: {'description': 'User not found'}
    }
})
def get_user(user_id):
    return users_service.get_user(user_id, request)

@users_bp.route('/users/<int:user_id>', methods=['PUT'])
@swag_from({
    'tags': ['User'],
    'summary': 'Update User',
    'description': 'Updates the details of an existing user.',
    'parameters': [
        {
            'name': 'user_id',
            'in': 'path',  # <---- This tells Swagger that user_id is in the URL
            'required': True,
            'type': 'integer',
            'description': 'The ID of the user who is being updated'
        },
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'username': {'type': 'string', 'description': 'New username'},
                    'password': {'type': 'string', 'description': 'New user password'}
                }
            }
        }
    ],
    'responses': {
        200: {'description': 'User updated successfully'},
        400: {'description': 'Bad request'}
    }
})
def update_user(user_id):
    data = request.get_json()
    if not data:
        return {"error": "Missing data for update."}, 400
    return users_service.update_user(user_id, data)

@users_bp.route('/users/<int:user_id>', methods=['DELETE'])
@swag_from({
    'tags': ['User'],
    'summary': 'Delete User',
    'description': 'Deletes a user from the system.',
    'parameters': [
        {
            'name': 'user_id',
            'in': 'path',  # <---- This tells Swagger that user_id is in the URL
            'required': True,
            'type': 'integer',
            'description': 'The ID of the user who is being deleted'
        }
    ],
    'responses': {
        200: {'description': 'User deleted'},
        403: {'description': 'Unauthorized'},
        404: {'description': 'User not found'}
    }
})
def delete_user(user_id):
    res = validate_admin_request(request)
    if res:
        return res
    return users_service.delete_user(user_id)

@users_bp.route('/users/<int:user_id>/password', methods=['PUT'])
@swag_from({
    'tags': ['User'],
    'summary': 'Update User Password',
    'description': 'Updates the password of an existing user.',
    'parameters': [
        {
            'name': 'user_id',
            'in': 'path',  # <---- This tells Swagger that user_id is in the URL
            'required': True,
            'type': 'integer',
            'description': 'The ID of the user whose password is being updated'
        },
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'password': {'type': 'string', 'description': 'New user password'}
                }
            }
        }
    ],
    'responses': {
        200: {'description': 'Password updated successfully'},
        400: {'description': 'Bad request'},
        404: {'description': 'User not found'}
    }
})
def update_user_password(user_id):
    data = request.get_json()

    if not data or 'password' not in data:
        return {"error": "Missing password data."}, 400

    return users_service.update_password(user_id, data['password'])


### Customers ###

@customers_bp.route('/customers', methods=['POST'])
@swag_from({
    'tags': ['Customers'],
    'summary': 'Create a Customer',
    'description': 'Creates a new customer with the given details, including delivery and billing addresses.',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'company': {'type': 'string', 'description': 'Company name of the customer'},
                    'account_number': {'type': 'string', 'description': 'Customer account number'},
                    'tax_number': {'type': 'string', 'description': 'Tax number of the customer'},
                    'contact1': {'type': 'string', 'description': 'Primary contact person', 'required': True},
                    'contact2': {'type': 'string', 'description': 'Secondary contact person'},
                    'contact3': {'type': 'string', 'description': 'Third contact person'},
                    'phone1': {'type': 'string', 'description': 'Primary phone number'},
                    'phone2': {'type': 'string', 'description': 'Secondary phone number'},
                    'phone3': {'type': 'string', 'description': 'Third phone number'},
                    'email1': {'type': 'string', 'description': 'Primary email address', 'required': True},
                    'email2': {'type': 'string', 'description': 'Secondary email address'},
                    'email3': {'type': 'string', 'description': 'Third email address'},
                    'private': {'type': 'boolean', 'description': 'Indicates if the customer is private'},
                    'notes': {'type': 'string', 'description': 'Additional notes about the customer'},
                    'delivery_address': {
                        'type': 'object',
                        'description': 'Delivery address details',
                        'properties': {
                            'street': {'type': 'string', 'description': 'Street name', 'required': True},
                            'house_number': {'type': 'string', 'description': 'House number', 'required': True},
                            'postal_code': {'type': 'string', 'description': 'Postal code', 'required': True},
                            'city': {'type': 'string', 'description': 'City name'},
                            'country': {'type': 'string', 'description': 'Country name'}
                        }
                    },
                    'billing_address': {
                        'type': 'object',
                        'description': 'Billing address details',
                        'properties': {
                            'street': {'type': 'string', 'description': 'Street name', 'required': True},
                            'house_number': {'type': 'string', 'description': 'House number', 'required': True},
                            'postal_code': {'type': 'string', 'description': 'Postal code', 'required': True},
                            'city': {'type': 'string', 'description': 'City name'},
                            'country': {'type': 'string', 'description': 'Country name'}
                        }
                    }
                }
            }
        }
    ],
    'responses': {
        201: {'description': 'Customer created successfully'},
        400: {'description': 'Bad request - missing or incorrect data'}
    }
})
def create_customer():
    return customers_service.create_customer(request)

@customers_bp.route('/customers', methods=['GET'])
@swag_from({
    'tags': ['Customers'],
    'summary': 'Get Customers',
    'description': 'Retrieves all customers from the system.',
    'responses': {
        200: {'description': 'A list of customers'}
    }
})
def get_customers():
    return customers_service.get_customers(request)

@customers_bp.route('/customers/<int:customer_id>', methods=['GET'])
@swag_from({
    'tags': ['Customers'],
    'summary': 'Get Customer by ID',
    'description': 'Retrieve details of a specific customer.',
    'parameters': [{
        'name': 'customer_id',
        'in': 'path',
        'required': True,
        'type': 'integer',
        'description': 'The ID of the customer'
    }],
    'responses': {
        200: {'description': 'Customer details'},
        404: {'description': 'Customer not found'}
    }
})
def get_customer(customer_id):
    return customers_service.get_customer(customer_id, request)

@customers_bp.route('/customers/<int:customer_id>', methods=['PUT'])
@swag_from({
    'tags': ['Customers'],
    'summary': 'Update Customer',
    'description': 'Updates the details of an existing customer, including their contact information and addresses (both delivery and billing).',
    'parameters': [
        {
            'name': 'customer_id',
            'in': 'path',
            'required': True,
            'type': 'integer',
            'description': 'The ID of the customer who is being updated'
        },
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'company': {'type': 'string', 'description': 'The company name of the customer'},
                    'account_number': {'type': 'string', 'description': 'The account number of the customer'},
                    'tax_number': {'type': 'string', 'description': 'The tax number of the customer'},
                    'contact1': {'type': 'string', 'description': 'Primary contact information for the customer'},
                    'contact2': {'type': 'string', 'description': 'Secondary contact information for the customer (optional)'},
                    'contact3': {'type': 'string', 'description': 'Tertiary contact information for the customer (optional)'},
                    'phone1': {'type': 'string', 'description': 'Primary phone number for the customer'},
                    'phone2': {'type': 'string', 'description': 'Secondary phone number for the customer (optional)'},
                    'phone3': {'type': 'string', 'description': 'Tertiary phone number for the customer (optional)'},
                    'email1': {'type': 'string', 'description': 'Primary email for the customer'},
                    'email2': {'type': 'string', 'description': 'Secondary email for the customer (optional)'},
                    'email3': {'type': 'string', 'description': 'Tertiary email for the customer (optional)'},
                    'private': {'type': 'boolean', 'description': 'Indicates whether the customer is a private customer'},
                    'notes': {'type': 'string', 'description': 'Additional notes about the customer (optional)'},
                    'delivery_address': {
                        'type': 'object',
                        'properties': {
                            'street': {'type': 'string', 'description': 'Street address for delivery'},
                            'house_number': {'type': 'string', 'description': 'House number for delivery'},
                            'postal_code': {'type': 'string', 'description': 'Postal code for delivery'},
                            'city': {'type': 'string', 'description': 'City for delivery'},
                            'country': {'type': 'string', 'description': 'Country for delivery'}
                        },
                        'description': 'The delivery address of the customer'
                    },
                    'billing_address': {
                        'type': 'object',
                        'properties': {
                            'street': {'type': 'string', 'description': 'Street address for billing'},
                            'house_number': {'type': 'string', 'description': 'House number for billing'},
                            'postal_code': {'type': 'string', 'description': 'Postal code for billing'},
                            'city': {'type': 'string', 'description': 'City for billing'},
                            'country': {'type': 'string', 'description': 'Country for billing'}
                        },
                        'description': 'The billing address of the customer'
                    }
                }
            }
        }
    ],
    'responses': {
        200: {'description': 'Customer updated successfully'},
        400: {'description': 'Bad request, invalid input data or missing required fields'},
        404: {'description': 'Customer not found'}
    }
})
def update_customer(customer_id):
    data = request.get_json()
    if not data:
        return {"error": "Fehlende Daten für das Update."}, 400
    return customers_service.update_customer(customer_id, data)

@customers_bp.route('/customers/<int:customer_id>', methods=['DELETE'])
@swag_from({
    'tags': ['Customers'],
    'summary': 'Delete Customer',
    'description': 'Deletes a customer from the system.',
    'parameters': [
        {
            'name': 'customer_id',
            'in': 'path',
            'required': True,
            'type': 'integer',
            'description': 'The ID of the customer to be deleted'
        }
    ],
    'responses': {
        200: {'description': 'Customer deleted'},
        404: {'description': 'Customer not found'}
    }
})
def delete_customer(customer_id):
    return customers_service.delete_customer(customer_id)

### Contract ###
@contracts_bp.route('/contracts', methods=['POST'])
def create_contract():
    return contracts_service.create_contract(request)

@contracts_bp.route('/contracts', methods=['GET'])
def get_contracts():
    return contracts_service.get_contracts(request)

@contracts_bp.route('/contracts/<int:contract_id>', methods=['GET'])
def get_contract(contract_id):
    return contracts_service.get_contract_by_id(contract_id, request)

@contracts_bp.route('/contracts/<int:contract_id>', methods=['PUT'])
def update_contract(contract_id):
    data = request.get_json()
    if not data:
        return {"error": "Fehlende Daten für das Update."}, 400
    return contracts_service.update_contract(contract_id, data)

@contracts_bp.route('/contracts/<int:contract_id>', methods=['DELETE'])
def delete_contract(contract_id):
    return contracts_service.delete_contract(contract_id)


### ware ###
@wares_bp.route('/wares', methods=['POST'])
def create_ware():
    return wares_service.create_ware(request)

@wares_bp.route('/wares', methods=['GET'])
def get_wares():
    return wares_service.get_wares(request)

@wares_bp.route('/wares/<int:ware_id>', methods=['GET'])
def get_ware(ware_id):
    return wares_service.get_ware_by_id(ware_id, request)

@wares_bp.route('/wares/<int:ware_id>', methods=['PUT'])
def update_ware(ware_id):
    data = request.get_json()
    if not data:
        return {"error": "Fehlende Daten für das Update."}, 400
    return wares_service.update_ware(ware_id, data)

@wares_bp.route('/wares/<int:ware_id>', methods=['DELETE'])
def delete_ware(ware_id):
    return wares_service.delete_ware(ware_id)
