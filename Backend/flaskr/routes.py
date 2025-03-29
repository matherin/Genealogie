from urllib import response
from flask import Blueprint, request, jsonify, redirect, url_for
from .database import db
from .datamodels import *
from .request_handling import accounts_service, location_service, groups_service, orders_service, helper_functions, auth_service, invoice_service, meals_service
from .auth.validate_request import validate_admin_request, validate_location_request, validate_group_request
from datetime import datetime

# Blueprints
accounts_bp = Blueprint('accounts', __name__, url_prefix='/api')
group_bp = Blueprint('group', __name__, url_prefix='/api' )
location_bp = Blueprint('location', __name__, url_prefix='/api' )
additional_bp = Blueprint('additional', __name__, url_prefix='/api' )
meal_bp = Blueprint('meal', __name__, url_prefix='/api')
auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')
invoice_bp = Blueprint('invoice', __name__, url_prefix='/api/invoice')

### Abrechnung ###
# route for the generating an invoice of an user
@invoice_bp.route("/<year>/<month>/user/<id>", methods=["GET"])
def user_invoice(year, month, id):
    res = validate_admin_request(request)
    if res:
        return res 
    return invoice_service.get_user_invoice(year, month, id)

# route for the generating an invoice of a group
@invoice_bp.route("/<year>/<month>/group/<id>", methods=["GET"])
def group_invoice(year, month, id):
    res = validate_admin_request(request)
    if res:
        return res 
    return invoice_service.get_group_invoice(year, month, id)

# route for the generating an invoice of a location
@invoice_bp.route("/<year>/<month>/location/<id>", methods=["GET"])
def location_invoice(year, month, id):
    res = validate_admin_request(request)
    if res:
        return res 
    return invoice_service.get_location_invoice(year, month, id)

### Authentication ###
# route for the reception of the credentials and login handling
@auth_bp.route("/login", methods=['POST'])
def user_login():
    return auth_service.handle_login_request(request)

### Accounts ###
# Route fuer das Erstellen eines neuen Accounts ohne Hashing
@accounts_bp.route('/accounts', methods=['POST'])
def create_account_route():
    res = validate_admin_request(request)
    if res:
        return res 
    return accounts_service.create_account(request) 

# Route fuer das Abrufen aller Accounts
@accounts_bp.route('/accounts', methods=['GET'])
def get_accounts():
    return accounts_service.get_accounts(request)

# Route fuer das Abrufen eines Accounts nach ID
@accounts_bp.route('/accounts/<account_id>', methods=['GET'], endpoint='get_account')
def get_account(account_id):
    # Überprüfe, ob account_id ein Integer ist
    try:
        account_id = int(account_id)
    except ValueError:
        return jsonify({"error": "Invalid account ID provided."}), 400

    return accounts_service.get_account_by_id(account_id, request)

# Route für das Aktualisieren eines Accounts
@accounts_bp.route('/accounts/<int:account_id>', methods=['PUT'], endpoint='update_account')
def update_account_route(account_id):
    data = request.get_json()  
    if not data:
        return {"error": "Fehlende Daten für das Konto-Update."}, 400

    return accounts_service.update_account(account_id, data)

# Route fuer das Loeschen eines Accounts
@accounts_bp.route('/accounts/<int:account_id>', methods=['DELETE'], endpoint='delete_account')
def delete_account(account_id):
    res = validate_admin_request(request)
    if res:
        return res 
    return accounts_service.delete_account(account_id)

# Route fuer das Abrufen der aktuellen Bestellung eines Accounts
@accounts_bp.route('/account/<int:account_id>/order', methods=['GET'])
def get_current_order_route(account_id):
    return orders_service.get_account_order(account_id, request)

# Route fuer das Aktualisieren einer Bestellung eines Accounts
@accounts_bp.route('/account/<int:account_id>/order', methods=['PUT', 'POST'], endpoint='update_order')
def update_order_route(account_id):
    return orders_service.put_account_order(account_id, request)

### Location ###
@location_bp.route('/locations', methods=['GET'], endpoint='get_locations')
def get_all_locations():
    return location_service.get_all_locations(request)

@location_bp.route('/locations', methods=['POST'])
def create_location():
    res = validate_admin_request(request)
    if res:
        return res 
    response, code = location_service.create_location(request)

    return response, code

@location_bp.route('/location/<id>', methods=['DELETE'])
def delete_location(id):
    res = validate_admin_request(request)
    if res:
        return res 
    response, code = location_service.delete_location(id)

    return response, code



@location_bp.route('/locations/<id>/groups', methods=['GET'], endpoint='get_location_groups')
def get_location_groups(id):
    if not id.isdigit(): 
        return {"error": "Invalid location ID format."}, 400 

    response, status = location_service.get_groups_by_location_id(request, id)

    return response, status

@location_bp.route('/locations/orders', methods=['GET'])
def get_location_orders():
    
    res = validate_group_request(request)
    if res:
        return res 

    return location_service.get_location_orders(request)


@location_bp.route('/locations/<id>/members', methods=['GET'], endpoint='get_members')
def get_members(id):
    res = validate_location_request(request)
    if res:
        return res 
    return location_service.get_users(id)

@location_bp.route("/locations/<int:location_id>/name", methods=["GET"])
def get_location_name(location_id):
    return location_service.get_location_name_by_id(location_id)


### Group ###
@group_bp.route('/groups', methods=['GET'], endpoint='get_groups')
def get_groups():
    res = validate_group_request(request)
    if res:
        return res 
    return groups_service.get_all_groups(request)

@group_bp.route('/groups', methods=['POST'])
def create_group():
    res = validate_location_request(request)
    if res:
        return res 
    return groups_service.create_group(request)

@group_bp.route('/groups', methods=['DELETE'])
def delete_group():
    res = validate_location_request(request)
    if res:
        return res 
    return groups_service.delete_group(request)

@group_bp.route('/groups/<int:group_id>', methods=['GET'], endpoint='get_group')
def get_group(group_id):
    res = validate_group_request(request)
    if res:
        return res 
    return groups_service.get_group_by_id(group_id, request)

@group_bp.route('/groups/<int:group_id>', methods=['PUT'], endpoint='change_group_name')
def change_group_name(group_id):
    res = validate_group_request(request)
    if res:
        return res 
    return groups_service.change_group_name(group_id, request)

@group_bp.route('/groups/leaders/<id>', methods=['GET'])
def get_groups_by_leader_id(id):
    leader_id = str(id)

    res = validate_group_request(request)
    if res:
        return res
    
    return groups_service.get_groups_by_leader_id(leader_id, request)
    
@group_bp.route('/groups/<int:group_id>/members', methods=['GET'], endpoint='get_group_members')
def get_group_members(group_id):
    res = validate_group_request(request)
    if res:
        return res 
    return groups_service.get_group_members(group_id)

@group_bp.route('/groups/<int:group_id>/leader', methods=['GET'], endpoint='get_group_leader')
def get_group_members(group_id):
    res = validate_group_request(request)
    if res:
        return res 
    return groups_service.get_group_leader(group_id)

@group_bp.route('/groups/<int:group_id>/leader', methods=['PUT'], endpoint='set_group_leader')
def set_group_leader(group_id):
    res = validate_group_request(request)
    if res:
        return res 
    return groups_service.set_group_leader(group_id, request)

@group_bp.route('/groups/<int:group_id>/leader', methods=['DELETE'], endpoint='remove_group_leader')
def set_group_leader(group_id):
    res = validate_group_request(request)
    if res:
        return res 
    return groups_service.remove_group_leader(group_id, request)

@group_bp.route('/groups/<int:group_id>/order', methods=['GET'], endpoint='get_group_order')
def get_group_order(group_id):
    res = validate_group_request(request)
    if res:
        return res 
    return orders_service.get_group_order(group_id, request)

@group_bp.route('/groups/<int:group_id>/order', methods=['POST'], endpoint='set_group_order')
def set_group_order(group_id):
    res = validate_group_request(request)
    if res:
        return res 
    return orders_service.put_group_order(group_id, request)

@group_bp.route('/groups/<int:group_id>/order', methods=['PUT', 'OPTIONS'], endpoint='update_group_order')
def put_group_order(group_id):
    res = validate_group_request(request)
    if res:
        return res 
    return orders_service.put_group_order(group_id, request)

@accounts_bp.route('/account/<int:account_id>/groups', methods=['PUT', 'POST'], endpoint='update_groups')
def update_groups_route(account_id):
    # Berechtigungsprüfung
    res = validate_group_request(request)
    if res:
        return res 

    return groups_service.update_account_groups(account_id, request)

@group_bp.route('/groups/leaders/info', methods=['GET'])
def get_all_group_leaders():
    try:
        
        leaders = db.session.query(GroupLeader.leader_id).all()
        leader_ids = [leader[0] for leader in leaders]
        return jsonify(leader_ids), 200

    except Exception as e:
        print(f"Fehler: {e}") 
        return jsonify({"error": "Internal Server Error", "message": str(e)}), 500



### Meal Routes ###
@meal_bp.route('/meals', methods=['GET'])
def get_meals_route():
    return meals_service.get_meals()

@meal_bp.route('/meals', methods=['POST'])
def create_meal_route():
    res = validate_admin_request(request)
    if res:
        return res 
    return meals_service.create_meal(request)

@meal_bp.route('/meals/<int:meal_id>', methods=['GET'])
def get_meal_route(meal_id):
    return meals_service.get_meal(meal_id)

@meal_bp.route('/meals/<int:meal_id>', methods=['PUT'])
def update_meal_route(meal_id):
    res = validate_admin_request(request)
    if res:
        return res 
    return meals_service.update_meal(meal_id, request)

@meal_bp.route('/meals/<int:meal_id>', methods=['DELETE'])
def delete_meal_route(meal_id):
    res = validate_admin_request(request)
    if res:
        return res 
    return meals_service.delete_meal(meal_id)


### Additional

# Route für Upload CSV-Datei
@additional_bp.route('/upload', methods=['POST'])
def upload_csv():
    res = validate_admin_request(request)
    if res:
        return res 
    return helper_functions.handle_csv_import(request)
