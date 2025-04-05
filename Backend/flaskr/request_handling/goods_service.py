from os import name
from flask import jsonify
from sqlalchemy import *
from ..datamodels import *
from ..database import db


def create_good(request):
    data = request.get_json()

    # Check if data is provided
    if not data:
        return {"error": "Goods data is missing."}, 400

    # Extract and clean fields
    description = data.get("description", "").strip()
    price = data.get("price")
    unit = data.get("unit", "").strip()
    waste_code = data.get("waste_code", "").strip() or None
    collection_group = data.get("collection_group", "").strip() or None
    category = data.get("category", "").strip() or None
    tax_class = data.get("tax_class", "").strip() or None

    # Validate required fields
    if not description or price is None or not unit:
        return {"error": "Missing required fields (description, price, unit)."}, 400

    try:
        price = float(price)
    except ValueError:
        return {"error": "Invalid price format."}, 400

    # Create new goods instance
    new_good = Good(
        description=description,
        price=price,
        unit=unit,
        waste_code=waste_code,
        collection_group=collection_group,
        category=category,
        tax_class=tax_class
    )

    # Add to database and commit
    db.session.add(new_good)
    db.session.commit()

    # Return success response
    return {"success": "Goods created successfully", "id": new_good.id}, 201


def get_goods(request):
    goods = Good.query.all()
    return jsonify([good.to_dict() for good in goods]), 200

def get_good(id, request):
    good = Good.query.filter_by(id=id).first()

    if not good:
        return {"error": "Good not found"}, 404 

    return jsonify(good.to_dict()), 200

def update_good(good_id, data):
    # Fetch the good from the database by ID
    good = Good.query.get(good_id)
    if not good:
        return jsonify({"error": "Good not found"}), 404

    # Update fields if present in the input data
    if "bezeichnung" in data:
        good.description = data["bezeichnung"]
    if "preis" in data:
        good.price = data["preis"]
    if "einheit" in data:
        good.unit = data["einheit"]
    if "abfallschlüssel" in data:
        good.waste_code = data["abfallschlüssel"]
    if "sammelgruppe" in data:
        good.collection_group = data["sammelgruppe"]
    if "kategorie" in data:
        good.category = data["kategorie"]
    if "steuerklasse" in data:
        good.tax_class = data["steuerklasse"]

    # Commit the changes to the database
    db.session.commit()

    return jsonify({"success": "Good updated successfully"}), 200

def delete_good(good_id):
    good = Good.query.get(good_id)
    print("Tried getting good with ID", good_id, "but got", good, flush=True)

    if not good:
        return {"error": "Good not found"}, 404

    db.session.delete(good)
    db.session.commit()

    return {"success": "Good deleted successfully"}, 200
