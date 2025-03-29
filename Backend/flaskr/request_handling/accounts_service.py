from os import name
from flask import jsonify
from sqlalchemy import *
from ..datamodels import *
from ..database import db
import re
from flaskr.auth.password import get_hash

def create_account(request):
    data = request.get_json()
    if not data:
        return {"error": "Fehlende Daten für die Kontoerstellung."}, 400

    # Gültige Rollen definieren
    valid_roles = ["admin", "location", "group", "user"]

    # Rolle setzen oder auf Standardwert "standard_user" zurückfallen
    role = data.get("role", "user")
    if role not in valid_roles:
        return {"error": f"Ungültige Rolle: {role}. Gültige Rollen sind: {', '.join(valid_roles)}."}, 400

    # check if account has password
    if 'password' not in data:
        return {"error": "The account needs a password"}, 400

    # check if the password is well formed
    # ^[a-f0-9]{128}$ matches all hex strings of the length 128
    if not re.match(r"^[a-f0-9]{128}$", data['password']):
        return {"error": "The password hash is malformed"}, 400

    new_account = Account(
        vorname=data["vorname"],
        nachname=data["nachname"],
        password=data["password"],
        role=role
    )
    
    if "gruppe" in data:
        if not isinstance(data["gruppe"], list): 
            return {"error": "Account creation: Groups must be provided as an array of IDs"}, 400

        groups = Group.query.filter(Group.id.in_(data["gruppe"])).all()
        if len(groups) != len(data["gruppe"]):
            return {"error": "Some group IDs were not found"}, 404
        
        new_account.group = groups  # Account mit Gruppen verknüpfen

    if "standort" in data:
        if type(data["standort"]) != int:
            return {"error":"Account creation: Location ID must be an int"}, 400
        location = Location.query.get(data["standort"])
        if not location:
            return {"error":"Account creation: Location not found"}, 404
        new_account.location_id = data["standort"]

    # Nur Gruppen setzen, wenn die Rolle "group" ist
    if new_account.role == "group":
        if "led_groups" in data:
            new_account.led_groups_by_leader = data["led_groups"]
        else:
            # hotfix for test accounts
            if 'gruppe' in data:
                g = Group.query.filter(Group.id.in_(data["gruppe"])).all()
                new_account.led_groups_by_leader = g 


    db.session.add(new_account)
    db.session.commit()

    return {"success": "Kontoerstellung erfolgreich"}, 200

def update_account(account_id, data):
    account = Account.query.get(account_id)
    if not account:
        return jsonify({"error": "Account not found"}), 404

    # Persönliche Daten aktualisieren
    if "vorname" in data:
        account.vorname = data["vorname"]
    if "nachname" in data:
        account.nachname = data["nachname"]
    

    if 'password' in data:
        # gehastes Passwort ändern
        if not re.match(r"^[a-f0-9]{128}$", data['password']):
            return {"error": "The password hash is malformed"}, 400
        else: 
            account.password = data['password']
    
    if "role" in data:
        account.role = data["role"]

        if data['role'] == 'user':
            db.session.query(GroupLeader).filter_by(leader_id=account.id).delete()


    # Location aktualisieren
    if "location_id" in data:
        if data["location_id"] is not None: 
            location = Location.query.filter_by(id=data["location_id"]).first()
            if not location:
                return {"error": "Location not found"}, 400
            account.location_id = data["location_id"]
        else:
            account.location_id = None

    # Gruppen aktualisieren (mehrere Gruppen möglich)
    if "group_id" in data:
        group_ids = data["group_id"] if isinstance(data["group_id"], list) else [data["group_id"]]

        # Alle aktuellen Gruppenmitgliedschaften des Accounts entfernen
        db.session.query(GroupMembers).filter_by(member_id=account.id).delete()


        # hotfix to delete the user from the leaders
        if account.role == "group":
            db.session.query(GroupLeader).filter_by(leader_id=account.id).delete()

        # Alle übermittelten Gruppen hinzufügen
        for group_id in group_ids:
            group = Group.query.get(group_id)
            if not group:
                return {"error": f"Group {group_id} not found"}, 400

            if account.role == 'group':
                group_leader = GroupLeader(leader_id=account.id, group_id=group.id)
                db.session.add(group_leader)

            group_member = GroupMembers(member_id=account.id, group_id=group.id)
            db.session.add(group_member)
    
    db.session.add(account)
    db.session.commit()
    return {"success": "Account update successful"}, 200

def get_account_by_id(id, request):
    account = Account.query.filter_by(id=id).first()

    if not account:
        return {"error": "Account not found"}, 404 

    return jsonify(account.to_dict()), 200


def get_accounts(request):
    accounts = Account.query.all()
    return jsonify([account.to_dict() for account in accounts]), 200

def delete_account(account_id):
    account = Account.query.get(account_id)

    if not account:
        return {"error": "Account not found"}, 404 
    db.session.delete(account)
    db.session.commit()
    return {"success": "Account delete successfully"}, 200

def get_current_order(account_id):
    account = Account.query.get(account_id)

    if not account:
        print(f"Account with ID {account_id} not found.")
        return {"error": "Account not found"}, 404

    current_order = Order.query.filter_by(group_id=account.group_id).filter(Order.date == date.today()).first()

    if not current_order:
        return {"error": "No current order found for this account"}, 404

    order_data = {
        "order_id": current_order.id,
        "valid": True
    }



    return order_data, 200
