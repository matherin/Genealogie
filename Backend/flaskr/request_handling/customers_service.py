# from os import name
# from flask import jsonify
# from sqlalchemy import *
# from ..datamodels import *
# from ..database import db
# from datetime import datetime

# def create_location(request):
#     data = request.get_json()
    
#     # Überprüfen, ob die Daten vorhanden sind
#     if not data:
#         return {"error": "Data for location creation missing."}, 400
    
#     # Überprüfen, ob der Name des Standorts vorhanden und nicht leer ist
#     name = data.get("name", "").strip()
#     if not name:
#         return {"error": "Location name is required"}, 400

#     # Erstelle den neuen Standort und die zugehörige Gruppe
#     new_location = Location(name=name)
#     test_group = Group(name="test_group")

#     # Füge die Gruppe zur Liste der Gruppen des Standorts hinzu
#     new_location.groups = [test_group]

#     # Füge Standort und Gruppe zur Datenbank hinzu und committe die Transaktion
#     db.session.add(new_location)
#     db.session.add(test_group)
#     db.session.commit()

#     # Erfolgreiche Antwort zurückgeben
#     return {"success": "Location creation successful", "id": new_location.id}, 201  

# def delete_location(location_id):
#     location = Location.query.get(location_id)
#     print("tried getting location with id", location_id, "but got", location, flush=True)

#     if not location:
#         return {"error": "Location not found"}, 404 
#     db.session.delete(location)
#     db.session.commit()
#     return {"success": "Location delete successfully"}, 200


# def get_groups_by_location_id(request, id):
#     location = Location.query.get(id)
#     if not location:
#         return {"error":"Could not find location given by id"}, 400
    
#     groups = [group.to_dict() for group in location.groups]
    
#     return jsonify(groups), 200
    
# def get_users(id):
#     location = Location.query.get(id)
#     if not location:
#         return {"error":"Could not find location given by id"}, 404

#     res = [{"vorname":x.vorname, "nachname":x.nachname, "id":x.id, "rolle": x.role} for x in location.accounts]
#     return jsonify(res), 200


# def get_all_locations(request):
#     locations = Location.query.all()
#     locations = [location.to_dict() for location in locations]
#     return jsonify(locations), 200

# def get_location_orders(request):
#     date_str = request.args.get('date')
#     if not date_str:
#         return jsonify({"error": "Parameter 'date' fehlt"}), 400

#     try:
#         selected_date = datetime.strptime(date_str, "%Y-%m-%d").date()
#     except ValueError:
#         return jsonify({"error": "Ungültiges Datum"}), 400

#     locations = db.session.query(Location).all()

#     result = []
#     for location in locations:

#         group_orders = (
#             db.session.query(GroupOrder)
#             .filter(GroupOrder.date == selected_date)
#             .join(GroupOrder.group)
#             .filter(GroupOrder.group.has(location_id=location.id))
#             .all()
#         )

#         red_count = 0
#         blue_count = 0
#         green_count = 0

#         for group_order in group_orders:
#             for account_order in group_order.content: 
#                 if account_order.meal_id == 1:
#                     red_count += 1
#                 elif account_order.meal_id == 2:
#                     blue_count += 1
#                 elif account_order.meal_id == 3:
#                     green_count += 1
#                 elif account_order.meal_id == 4:
#                     red_count += 1
#                     green_count += 1
#                 elif account_order.meal_id == 5:
#                     blue_count += 1
#                     green_count += 1

#         result.append({
#             "id": location.id,
#             "name": location.name,
#             "order": [red_count, blue_count, green_count]
#         })

#     return jsonify(result)

# def get_location_name_by_id(location_id): 
#     location = Location.query.get(location_id)

#     if not location:    
#         return {"error": "Could not find location given by id"}, 400

#     return {"location_id": location.id, "name": location.name}, 200
