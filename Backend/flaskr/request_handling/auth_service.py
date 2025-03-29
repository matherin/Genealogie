from flask import make_response, jsonify
from ..auth.jwt import generate_session_token
from sqlalchemy import *
from ..datamodels import *
from ..database import db
import re

def handle_login_request(request):
    data = request.get_json()

    if not data:
        return {"error": "Data for account creation missing."}, 400

    if 'name' not in data or 'password' not in data:
        return {"error": "Necessary field for login missing."}, 400

    if type(data['name']) != str:
        return {"error": "Name must be a string."}, 400

    if type(data['password']) != str:
        return {"error": "Password must be a string."}, 400

    if len(data['password']) == 0:
        return {"error": "Password can not be empty."}, 400
    
    if len(data['name']) == 0:
        return {"error": "Name can not be empty."}, 400

    # Split basierend auf Großbuchstaben
    name_parts = re.split(r'(?<=[a-zäöüß])(?=[A-ZÄÖÜ])', data['name'])
    if len(name_parts) != 2:
        return {"error": "Name must include a first and last name with proper capitalization."}, 400

    vorname, nachname = name_parts  # Vor- und Nachname extrahieren

    # Login-Abfrage in der Datenbank
    account = Account.query.filter_by(
        password=data['password'],
        vorname=vorname,
        nachname=nachname
    ).first()

    if not account:
        return {"error": "Username or password incorrect"}, 403

    # Session-Cookie generieren
    cookie = generate_session_token(account.role, account.id)
    resp = make_response(jsonify({'message': 'Login successful'}), 200)
    resp.set_cookie('Session', cookie)
    return resp



