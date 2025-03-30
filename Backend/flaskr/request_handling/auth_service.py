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

    if 'username' not in data or 'password' not in data:
        return {"error": "Necessary field for login missing."}, 400

    if type(data['username']) != str:
        return {"error": "Name must be a string."}, 400

    if type(data['password']) != str:
        return {"error": "Password must be a string."}, 400

    if len(data['password']) == 0:
        return {"error": "Password can not be empty."}, 400
    
    if len(data['username']) == 0:
        return {"error": "Name can not be empty."}, 400

    # Login-Abfrage in der Datenbank
    user = User.query.filter_by(
        password=data['password'],
        username=data['username'],
    ).first()

    if not user:
        return {"error": "Username or password incorrect"}, 403

    # Session-Cookie generieren
    cookie = generate_session_token(user.role, user.id)
    resp = make_response(jsonify({'message': 'Login successful'}), 200)
    resp.set_cookie('Session', cookie)
    return resp



