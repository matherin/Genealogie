from urllib import response
from flask import Blueprint, request, jsonify, redirect, url_for
from .database import db
from .datamodels import *
from .request_handling import contracts_service, customers_service, auth_service, users_service, wares_service
from .auth.validate_request import validate_admin_request, validate_location_request, validate_group_request
from datetime import datetime

# Blueprints
users_bp = Blueprint('users', __name__, url_prefix='/api')
customers_bp = Blueprint('customers', __name__, url_prefix='/api' )
contracts_bp = Blueprint('contracts', __name__, url_prefix='/api' )
wares_bp = Blueprint('wares', __name__, url_prefix='/api' )
auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

### Authentication ###
# route for the reception of the credentials and login handling
@auth_bp.route("/login", methods=['POST'])
def user_login():
    return auth_service.handle_login_request(request)

### User ###
@users_bp.route('/users', methods=['POST'])
def create_user():
    res = validate_admin_request(request)
    if res:
        return res
    return users_service.create_user(request)

@users_bp.route('/users', methods=['GET'])
def get_users():
    return users_service.get_users(request)

@users_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    return users_service.get_user_by_id(user_id, request)

@users_bp.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    if not data:
        return {"error": "Fehlende Daten für das Update."}, 400
    return users_service.update_user(user_id, data)

@users_bp.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    res = validate_admin_request(request)
    if res:
        return res
    return users_service.delete_user(user_id)


### Customer ###
@customers_bp.route('/customers', methods=['POST'])
def create_customer():
    return customers_service.create_customer(request)

@customers_bp.route('/customers', methods=['GET'])
def get_customers():
    return customers_service.get_customers(request)

@customers_bp.route('/customers/<int:customer_id>', methods=['GET'])
def get_customer(customer_id):
    return customers_service.get_customer_by_id(customer_id, request)

@customers_bp.route('/customers/<int:customer_id>', methods=['PUT'])
def update_customer(customer_id):
    data = request.get_json()
    if not data:
        return {"error": "Fehlende Daten für das Update."}, 400
    return customers_service.update_customer(customer_id, data)

@customers_bp.route('/customers/<int:customer_id>', methods=['DELETE'])
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
