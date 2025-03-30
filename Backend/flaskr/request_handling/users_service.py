from os import name
from flask import jsonify
from sqlalchemy import *
from ..datamodels import *
from ..database import db
import re
from flaskr.auth.password import get_hash

def create_user(request):
    data = request.get_json()
    if not data:
        return {"error": "Fehlende Daten für die Kontoerstellung."}, 400

    # Gültige Rollen definieren
    valid_roles = ["admin", "user"]

    # Rolle setzen oder auf Standardwert "standard_user" zurückfallen
    role = data.get("role", "username")
    if role not in valid_roles:
        return {"error": f"Ungültige Rolle: {role}. Gültige Rollen sind: {', '.join(valid_roles)}."}, 400

    # check if account has password
    if 'password' not in data:
        return {"error": "The account needs a password"}, 400

    # check if the password is well formed
    # ^[a-f0-9]{128}$ matches all hex strings of the length 128
    # if not re.match(r"^[a-f0-9]{128}$", data['password']):
    #     return {"error": "The password hash is malformed"}, 400

    new_user = User(
        username=data["username"],
        password=data["password"],
        role=role
    )

    db.session.add(new_user)
    db.session.commit()

    return {"success": "Kontoerstellung erfolgreich"}, 200

def update_user(user_id, data):
    user = User.query.get(user_id)
    if not User:
        return jsonify({"error": "User not found"}), 404

    # Persönliche Daten aktualisieren
    if "username" in data:
        user.username = data["username"]
    

    if 'password' in data:
        # gehastes Passwort ändern
        # if not re.match(r"^[a-f0-9]{128}$", data['password']):
        #     return {"error": "The password hash is malformed"}, 400
        # else: 
        user.password = data['password']

    db.session.add(user)
    db.session.commit()
    return {"success": "Account update successful"}, 200

def update_password(user_id, new_password):
    user = User.query.get(user_id)
    
    if not user:
        return {"error": "User not found"}, 404

    user.password = new_password
    db.session.commit()

    return {"message": "Password updated successfully"}, 200

def get_user(id, request):
    user = User.query.filter_by(id=id).first()

    if not user:
        return {"error": "Account not found"}, 404 

    return jsonify(user.to_dict()), 200


def get_users(request):
    users = User.query.all()
    return jsonify([user.to_dict() for user in users]), 200

def delete_user(user_id):
    user = User.query.get(user_id)

    if not user:
        return {"error": "Account not found"}, 404 
    db.session.delete(user)
    db.session.commit()
    return {"success": "Account delete successfully"}, 200
