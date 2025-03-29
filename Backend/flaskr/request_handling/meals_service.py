from os import name
from flask import jsonify
from sqlalchemy import *
from ..datamodels import *
from ..database import db

def create_meal(request):
    data = request.get_json()
    if not data:
        return {"error": "Fehlende Daten für die Mahlzeiterstellung."}, 400

    custom_id = data.get('meal_id')
    if custom_id is not None:
        if Meal.query.get(custom_id):
            return {"error": "Meal-ID existiert bereits"}, 400

    if 'price' not in data:
        return {"error": "Preis ist erforderlich"}, 400

    try:
        price = float(data['price'])
        if price <= 0:
            return {"error": "Preis muss positiv sein"}, 400
    except ValueError:
        return {"error": "Ungültiger Preis"}, 400

    new_meal = Meal(
        id=custom_id,  
        price=price
    )

    db.session.add(new_meal)
    db.session.commit()

    return {"success": "Mahlzeit erstellt", "meal_id": new_meal.id}, 201


def update_meal(meal_id, request):
    data = request.get_json()
    meal = Meal.query.get(meal_id)
    
    if not meal:
        return {"error": "Mahlzeit nicht gefunden"}, 404

    if 'price' in data:
        try:
            new_price = float(data['price'])
            if new_price <= 0:
                raise ValueError
            meal.price = new_price
        except (ValueError, TypeError):
            return {"error": "Ungültiger Preiswert. Muss eine positive Zahl sein"}, 400

    db.session.commit()
    return {"success": "Mahlzeit erfolgreich aktualisiert"}, 200

def delete_meal(meal_id):
    meal = Meal.query.get(meal_id)
    
    if not meal:
        return {"error": "Mahlzeit nicht gefunden"}, 404

    db.session.delete(meal)
    db.session.commit()
    return {"success": "Mahlzeit erfolgreich gelöscht"}, 200

def get_meal(meal_id):
    meal = Meal.query.get(meal_id)
    
    if not meal:
        return {"error": "Mahlzeit nicht gefunden"}, 404

    return jsonify(meal.to_dict()), 200

def get_meals():
    meals = Meal.query.all()
    return jsonify([meal.to_dict() for meal in meals]), 200