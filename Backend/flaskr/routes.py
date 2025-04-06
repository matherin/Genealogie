from urllib import response
from flask import Blueprint, request, jsonify, redirect, url_for
from flasgger import swag_from
from .database import db
from .datamodels import *
from .request_handling import contracts_service, customers_service, auth_service, users_service, goods_service
from .auth.validate_request import validate_admin_request

# Blueprints
users_bp = Blueprint('users', __name__, url_prefix='/api')
customers_bp = Blueprint('customers', __name__, url_prefix='/api')
contracts_bp = Blueprint('contracts', __name__, url_prefix='/api')
goods_bp = Blueprint('goods', __name__, url_prefix='/api')
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
    'parameters' : [{
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'username': {'type': 'string', 'description': 'New username'},
                    'password': {'type': 'string', 'description': 'New user password'},
                    'role': {'type': 'string', 'description': 'New role', 'example': 'user'}
                }
            }
        }],
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
                    'password': {'type': 'string', 'description': 'New user password'},
                    'role': {'type': 'string', 'description': 'New user role'}
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
                    'contacts': {
                        'type': 'array',
                        'description': 'List of contact persons (up to 3 contacts)',
                        'maxItems': 3,
                        'items': {
                            'type': 'string',
                            'example': 'John Doe'
                        },
                        'example': ['John Doe', 'Jane Smith', 'Alice Johnson']
                    },
                    'phone_numbers': {
                        'type': 'array',
                        'description': 'List of phone numbers (up to 3 phone numbers)',
                        'maxItems': 3,
                        'items': {
                            'type': 'string',
                            'example': '+1234567890'
                        },
                        'example': ['+1234567890', '+1987654321', '+1122334455']
                    },
                    'emails': {
                        'type': 'array',
                        'description': 'List of email addresses (up to 3 emails)',
                        'maxItems': 3,
                        'items': {
                            'type': 'string',
                            'example': 'email@example.com'
                        },
                        'example': ['john.doe@example.com', 'jane.smith@example.com', 'alice.johnson@example.com']
                    },
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
                    'contacts': {
                        'type': 'array',
                        'description': 'List of contact persons (up to 3 contacts)',
                        'maxItems': 3,
                        'items': {
                            'type': 'string',
                            'example': 'John Doe'
                        },
                        'example': ['John Doe', 'Jane Smith', 'Alice Johnson']
                    },
                    'phone_numbers': {
                        'type': 'array',
                        'description': 'List of phone numbers (up to 3 phone numbers)',
                        'maxItems': 3,
                        'items': {
                            'type': 'string',
                            'example': '+1234567890'
                        },
                        'example': ['+1234567890', '+1987654321', '+1122334455']
                    },
                    'emails': {
                        'type': 'array',
                        'description': 'List of email addresses (up to 3 emails)',
                        'maxItems': 3,
                        'items': {
                            'type': 'string',
                            'example': 'email@example.com'
                        },
                        'example': ['john.doe@example.com', 'jane.smith@example.com', 'alice.johnson@example.com']
                    },
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

### Goods ###
@goods_bp.route('/goods', methods=['POST'])
@swag_from({
    'tags': ['Goods'],
    'summary': 'Create Goods',
    'description': 'Creates a new goods entry with the given details.',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'description': {
                        'type': 'string',
                        'description': 'Description of the goods',
                        'example': 'Old electronics'
                    },
                    'price': {
                        'type': 'number',
                        'format': 'float',
                        'description': 'Price per unit',
                        'example': 50.00
                    },
                    'unit': {
                        'type': 'string',
                        'description': 'Unit of measurement',
                        'example': 'kg'
                    },
                    'waste_code': {
                        'type': 'string',
                        'description': 'Waste code for categorization',
                        'example': '123456'
                    },
                    'collection_group': {
                        'type': 'string',
                        'description': 'Collection group classification',
                        'example': 'Electronics'
                    },
                    'category': {
                        'type': 'string',
                        'description': 'Category of goods',
                        'example': 'E-waste'
                    },
                    'tax_class': {
                        'type': 'string',
                        'description': 'Applicable tax class',
                        'example': 'standard'
                    }
                },
                'required': ['description', 'price', 'unit']
            }
        }
    ],
    'responses': {
        201: {
            'description': 'Goods created successfully',
            'content': {
                'application/json': {
                    'example': {
                        'success': 'Goods created successfully',
                        'id': 1
                    }
                }
            }
        },
        400: {
            'description': 'Bad request - missing or invalid data',
            'content': {
                'application/json': {
                    'example': {
                        'error': 'Missing required fields (description, price, unit).'
                    }
                }
            }
        }
    }
})
def create_good():
    return goods_service.create_good(request)

@goods_bp.route('/goods', methods=['GET'])
@swag_from({
    'tags': ['Goods'],
    'summary': 'Get Goods',
    'description': 'Retrieves all goods from the system.',
    'responses': {
        200: {
            'description': 'A list of goods',
            'content': {
                'application/json': {
                    'example': [
                        {
                            'wid': 1,
                            'bezeichnung': 'Old electronics',
                            'preis': 50.0,
                            'einheit': 'kg',
                            'abfallschlüssel': '123456',
                            'sammelgruppe': 'Electronics',
                            'kategorie': 'E-waste'
                        }
                    ]
                }
            }
        }
    }
})
def get_goods():
    return goods_service.get_goods(request)

@goods_bp.route('/goods/<int:good_id>', methods=['GET'])
@swag_from({
    'tags': ['Goods'],
    'summary': 'Get Good by ID',
    'description': 'Retrieve details of a specific good.',
    'parameters': [
        {
            'name': 'good_id',
            'in': 'path',
            'required': True,
            'type': 'integer',
            'description': 'The ID of the good'
        }
    ],
    'responses': {
        200: {
            'description': 'Good details',
            'content': {
                'application/json': {
                    'example': {
                        'wid': 1,
                        'bezeichnung': 'Old electronics',
                        'preis': 50.0,
                        'einheit': 'kg',
                        'abfallschlüssel': '123456',
                        'sammelgruppe': 'Electronics',
                        'kategorie': 'E-waste'
                    }
                }
            }
        },
        404: {'description': 'Good not found'}
    }
})
def get_good(good_id):
    return goods_service.get_good(good_id, request)


@goods_bp.route('/goods/<int:good_id>', methods=['PUT'])
@swag_from({
    'tags': ['Goods'],
    'summary': 'Update Good',
    'description': 'Updates the details of an existing good.',
    'parameters': [
        {
            'name': 'good_id',
            'in': 'path',
            'required': True,
            'type': 'integer',
            'description': 'The ID of the good to update'
        },
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'description': {
                        'type': 'string',
                        'description': 'Description of the goods',
                        'example': 'Old electronics'
                    },
                    'price': {
                        'type': 'number',
                        'format': 'float',
                        'description': 'Price per unit',
                        'example': 50.00
                    },
                    'unit': {
                        'type': 'string',
                        'description': 'Unit of measurement',
                        'example': 'kg'
                    },
                    'waste_code': {
                        'type': 'string',
                        'description': 'Waste code for categorization',
                        'example': '123456'
                    },
                    'collection_group': {
                        'type': 'string',
                        'description': 'Collection group classification',
                        'example': 'Electronics'
                    },
                    'category': {
                        'type': 'string',
                        'description': 'Category of goods',
                        'example': 'E-waste'
                    },
                    'tax_class': {
                        'type': 'string',
                        'description': 'Applicable tax class',
                        'example': 'standard'
                    }
                },
                'required': ['description', 'price', 'unit']
            }
        }
    ],
    'responses': {
        200: {'description': 'Good updated successfully'},
        400: {'description': 'Bad request, invalid input data'},
        404: {'description': 'Good not found'}
    }
})
def update_good(good_id):
    data = request.get_json()
    if not data:
        return {"error": "Fehlende Daten für das Update."}, 400
    return goods_service.update_good(good_id, data)


@goods_bp.route('/goods/<int:good_id>', methods=['DELETE'])
@swag_from({
    'tags': ['Goods'],
    'summary': 'Delete Good',
    'description': 'Deletes a good from the system.',
    'parameters': [
        {
            'name': 'good_id',
            'in': 'path',
            'required': True,
            'type': 'integer',
            'description': 'The ID of the good to be deleted'
        }
    ],
    'responses': {
        200: {'description': 'Good deleted successfully'},
        404: {'description': 'Good not found'}
    }
})
def delete_good(good_id):
    return goods_service.delete_good(good_id)



### Contract ###
@contracts_bp.route('/contracts', methods=['POST'])
@swag_from({
    'tags': ['Contracts'],
    'summary': 'Create a Contract',
    'description': 'Creates a new contract linked to an existing customer and optionally associates goods with the contract.',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'customer_id': {
                        'type': 'integer',
                        'description': 'The ID of the customer the contract belongs to',
                        'required': True
                    },
                    'date': {
                        'type': 'string',
                        'description': 'The date of the contract in format DD-MM-YYYY',
                        'example': '30-03-2025',
                        'required': True
                    },
                    'input': {
                        'type': 'boolean',
                        'description': 'Indicates whether the contract is an input (True) or output (False)'
                    },
                    'goods': {
                        'type': 'array',
                        'description': 'List of goods associated with the contract',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'good_id': {
                                    'type': 'integer',
                                    'description': 'ID of the good to be linked to the contract',
                                    'required': True
                                },
                                'quantity': {
                                    'type': 'integer',
                                    'description': 'Quantity of the good in the contract',
                                    'required': True
                                }
                            }
                        }
                    }
                }
            }
        }
    ],
    'responses': {
        201: {'description': 'Contract created successfully'},
        400: {'description': 'Bad request - missing or incorrect data'},
        404: {'description': 'Customer or good not found'}
    }
})
def create_contract():
    return contracts_service.create_contract(request)

@contracts_bp.route('/contracts', methods=['GET'])
@swag_from({
    'tags': ['Contracts'],
    'summary': 'Get all Contracts',
    'description': 'Returns a list of all contracts including related customer information.',
    'responses': {
        200: {'description': 'List of contracts returned successfully'},
    }
})
def get_contracts():
    return contracts_service.get_contracts(request)

@contracts_bp.route('/contracts/<int:contract_id>', methods=['GET'])
@swag_from({
    'tags': ['Contracts'],
    'summary': 'Get a Contract by ID',
    'description': 'Returns the contract with the given ID along with associated customer information.',
    'parameters': [
        {
            'name': 'contract_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'The ID of the contract to retrieve'
        }
    ],
    'responses': {
        200: {'description': 'Contract found and returned successfully'},
        404: {'description': 'Contract not found'}
    }
})
def get_contract(contract_id):
    return contracts_service.get_contract(contract_id, request)

@contracts_bp.route('/contracts/<int:contract_id>', methods=['PUT'])
@swag_from({
    'tags': ['Contracts'],
    'summary': 'Update a Contract',
    'description': 'Updates an existing contract by its ID. You can update the customer, date, and whether it is an input contract.',
    'parameters': [
        {
            'name': 'contract_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'The ID of the contract to update'
        },
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'customer_id': {'type': 'integer', 'description': 'ID of the customer associated with this contract'},
                    'date': {'type': 'string', 'description': 'Date of the contract (DD-MM-YYYY)'},
                    'input': {'type': 'boolean', 'description': 'Indicates if the contract is an input contract'}
                }
            }
        }
    ],
    'responses': {
        200: {'description': 'Contract updated successfully'},
        400: {'description': 'Bad request - invalid data or IDs'},
        404: {'description': 'Contract not found'}
    }
})
def update_contract(contract_id):
    data = request.get_json()
    if not data:
        return {"error": "Fehlende Daten für das Update."}, 400
    return contracts_service.update_contract(contract_id, data)

@contracts_bp.route('/contracts/<int:contract_id>', methods=['DELETE'])
@swag_from({
    'tags': ['Contracts'],
    'summary': 'Delete a Contract',
    'description': 'Deletes a contract by its ID along with all associated goods from the contract.',
    'parameters': [
        {
            'name': 'contract_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'The ID of the contract to delete'
        }
    ],
    'responses': {
        200: {'description': 'Contract deleted successfully'},
        404: {'description': 'Contract not found'}
    }
})
def delete_contract(contract_id):
    return contracts_service.delete_contract(contract_id)