from os import name
from flask import jsonify
from sqlalchemy import *
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
from ..datamodels import *
from ..database import db
from .helper_functions import *


from datetime import datetime
from flask import jsonify, request
from sqlalchemy.exc import SQLAlchemyError

def put_group_order(group_id, request):
    """
    1) Datum validieren
    2) Gruppe holen
    3) GroupOrder holen/erstellen
    4) Orders verarbeiten (AccountOrder)
    5) Commit
    """
    # 1) Datum aus Request args
    order_date, error_response = _validate_and_extract_date(request)
    if error_response:
        return error_response

    # 2) Gruppe checken
    group = get_group_by_id(group_id)
    if not group:
        return jsonify({"error": "Group not found"}), 404

    # 3) Request Body checken
    data = request.get_json() or {}
    if 'orders' not in data:
        return jsonify({"error": "Invalid request format"}), 400

    try:
        # 4) GroupOrder holen oder erstellen
        group_order = _get_or_create_group_order(group_id, order_date)

        # 5) AccountOrders verarbeiten
        for order_item in data['orders']:
            account_id = order_item.get('account_id')
            meal_id = order_item.get('meal_id')
            valid_flag = order_item.get('valid')

            # Mitgliedschaft prüfen + AccountOrder holen/erstellen
            account_order, error_response = _process_account_order(
                group, 
                group_order, 
                account_id, 
                meal_id, 
                valid_flag
            )
            if error_response:
                return error_response

        db.session.commit()
        return jsonify({
            "message": "Group order updated/created successfully",
            "group_order_id": group_order.id,
            "date": order_date.isoformat()
        }), 201

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": f"Database error: {str(e)}"}), 500

def get_group_order(group_id, request):
    group = get_group_by_id(group_id)
    if not group:
        return jsonify({"error": "Group not found"}), 404

    date_str = request.args.get('date')
    if date_str:
        try:
            filter_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            return jsonify({"error": "Invalid date format. Use YYYY-MM-DD"}), 400

        orders_filtered = [o.to_dict() for o in group.group_orders if o.date == filter_date]
        return jsonify(orders_filtered), 200
    else:
        orders = [order.to_dict() for order in group.group_orders]
        return jsonify(orders), 200


def put_account_order(acc_id, request):
    # 1) JSON + Datum
    data, error_response = _parse_json(request)
    if error_response:
        return error_response

    date_str = request.args.get("date")
    if not date_str:
        order_date = date.today()
    else:
        try:
            order_date = datetime.strptime(date_str, "%Y-%m-%d").date()  # Fix: use date_str
        except ValueError:
            return jsonify({"error": "Invalid date format. Use YYYY-MM-DD"}), 400

    meal_id = data.get("meal_id")
    valid = data.get("valid", True)

    # 2) Account checken
    if not account_exists(acc_id):
        return jsonify({"error": "Account does not exist"}), 404

    account = get_account_by_id(acc_id)
    if not account:
        return jsonify({"error": "Account not found"}), 404

    # 3) Account-Gruppen (nur Member)
    user_groups = account.group
    if not user_groups:
        return jsonify({"error": "User is not in any group"}), 404

    primary_group = user_groups[0]

    # 4) GroupOrder suchen anhand des Datums
    group_order = GroupOrder.query.filter_by(
        group_id=primary_group.id,
        date=order_date
    ).first()

    if not group_order:
        return jsonify({"error": "No GroupOrder found for this date in user's first group"}), 404

    # 5) AccountOrder updaten oder anlegen
    try:
        existing_order = AccountOrder.query.filter_by(
            account_id=acc_id,
            group_order_id=group_order.id
        ).first()

        if existing_order:
            existing_order.meal_id = meal_id
            existing_order.valid = valid
        else:
            new_order = AccountOrder(
                account_id=acc_id,
                meal_id=meal_id,
                valid=valid,
                group_order_id=group_order.id
            )
            db.session.add(new_order)

        db.session.commit()
        return jsonify({"message": "AccountOrder updated/created successfully"}), 201

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": f"Database error: {str(e)}"}), 500

def get_account_order(acc_id, request):
    """
    GET /account/<acc_id>/order?date=YYYY-MM-DD
    - Filtert AccountOrders nach Datum
    """
    date_str = request.args.get("date")
    if not date_str:
        filter_date = date.today()
    else:
        try:
            filter_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            return jsonify({"error": "Invalid date format. Use YYYY-MM-DD"}), 400

    if not account_exists(acc_id):
        return jsonify({"error": "Account does not exist"}), 400

    account = get_account_by_id(acc_id)
    if not account:
        return jsonify({"error": "Account not found"}), 404

    orders_filtered = AccountOrder.query \
        .join(GroupOrder) \
        .filter(GroupOrder.date == filter_date, AccountOrder.account_id == acc_id) \
        .all()

    orders_list = [o.to_dict() for o in orders_filtered]
    return jsonify(orders_list), 200


# Helper functions
def _validate_and_extract_date(request):
    """Datum aus query-Param ziehen & validieren."""
    date_str = request.args.get('date')
    if not date_str:
        return None, (jsonify({"error": "Date parameter is required"}), 400)
    try:
        order_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        return order_date, None
    except ValueError:
        return None, (jsonify({"error": "Invalid date format. Use YYYY-MM-DD"}), 400)


def _get_or_create_group_order(group_id, order_date):
    """Bestehende GroupOrder für (group_id, date) holen oder neu erstellen."""
    existing = GroupOrder.query.filter_by(group_id=group_id, date=order_date).first()
    if existing:
        return existing
    new_order = GroupOrder(group_id=group_id, date=order_date)
    db.session.add(new_order)
    db.session.flush() 
    return new_order


def _process_account_order(group, group_order, account_id, meal_id, valid_flag):
    """
    - Account checken & Mitgliedschaft prüfen
    - Bestehende AccountOrder (account_id, group_order_id) aktualisieren oder neu anlegen
    """
    account = Account.query.get(account_id)
    if not account:
        return None, (jsonify({"error": f"Account {account_id} does not exist"}), 400)

    # Check if user is in group (Members oder Leaders)
    if account not in group.members and account not in group.leaders:
        return None, (jsonify({"error": f"Account {account_id} is not part of this group"}), 403)

    # AccountOrder checken
    existing_order = AccountOrder.query.filter_by(
        account_id=account_id, 
        group_order_id=group_order.id
    ).first()

    if existing_order:
        existing_order.meal_id = meal_id
        existing_order.valid = valid_flag
        return existing_order, None
    else:
        new_acc_order = AccountOrder(
            account_id=account_id,
            meal_id=meal_id,
            valid=valid_flag,
            group_order_id=group_order.id
        )
        db.session.add(new_acc_order)
        return new_acc_order, None

def _parse_json(request):
    """Liest JSON Body. Gibt (data, None) oder (None, (error_response, code)) zurück."""
    try:
        data = request.get_json()
        if not data:
            return None, (jsonify({"error": "Empty request body"}), 400)
        return data, None
    except:
        return None, (jsonify({"error": "Invalid JSON format"}), 400)


def _extract_date_from_json(data):
    """Zieht 'date' aus data und validiert es im YYYY-MM-DD-Format."""
    date_str = data.get("date")
    if not date_str:
        return None, (jsonify({"error": "Date is required"}), 400)
    try:
        parsed_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        return parsed_date, None
    except ValueError:
        return None, (jsonify({"error": "Invalid date format. Use YYYY-MM-DD"}), 400)

def account_exists(acc_id):
    """Prüft (boolean), ob ein Account existiert."""
    return Account.query.get(acc_id) is not None

def get_account_by_id(acc_id):
    """Liefert ein Account-Objekt oder None."""
    return Account.query.get(acc_id)
