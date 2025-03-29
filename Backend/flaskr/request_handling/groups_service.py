from os import name
from flask import jsonify
from sqlalchemy import *
from ..datamodels import *
from ..database import db

from dateutil import parser
from datetime import datetime, timezone

def create_group(request):
    data = request.get_json()
    
    if not data:
        return {"error":"Data for account creation missing."}, 400
    
    new_group = Group(
        name=data["name"],
        location_id=data["location"],
        )
    
    member_ids = data.get("members", [])
    if not isinstance(member_ids, list):
        return jsonify({"error": "Members müssen als List übergeben werden"}), 400

    for member_id in member_ids:
        account = Account.query.get(member_id)
        if account:
            new_group.members.append(account)
        else:
            return jsonify({"error": f"Account mit ID {member_id} nicht gefunden"}), 400
    

    leader_ids = data.get("leader", [])
    if not isinstance(member_ids, list):
        return jsonify({"error": "Leader müssen als List übergeben werden"}), 400
    elif not leader_ids:
        return jsonify({"error": "Leader müssen angeben werden"}), 400

    for leader_id in leader_ids:
        leader = Account.query.get(leader_id)

        if leader.role == "group":
            new_group.leaders.append(leader)
        else:
            return jsonify({"error": f"Account mit ID {leader_id} hat keine 'leader'-Rolle"}), 400
    

    db.session.add(new_group)
    db.session.commit()

    return {"success":"Group creation successful"}, 200


def get_all_groups(request):
    groups = Group.query.all()
    return jsonify([group.to_dict() for group in groups]), 200


def get_group_by_id(id, request):
    group = Group.query.get(id)

    if not group:
        return {"error":"Group not found"}, 404

    return jsonify(group.to_dict()), 200


def get_groups_by_leader_id(leader_id, request):
    
    # Query abfragen
    date_str = request.args.get('date')
    
    if not date_str:
        return jsonify({"error": "Parameter 'date' fehlt"}), 400

    try:
        selected_date = datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        return jsonify({"error": "Ungültiges Datum"}), 400

    groups = db.session.query(Group).all()

    result = []
    for group in groups:
        if not group.leaders:
            continue

        leader = group.leaders[-1]

        # Falls eine leader_id angegeben wurde:
        if leader_id and str(leader.id) != leader_id:
            continue  

        leader_account_order = next((order for order in leader.account_orders if order.group_order and order.group_order.date == selected_date), None)
        leader_order_value = leader_account_order.meal_id if leader_account_order else 6

        leader_data = {
            "id": leader.id,
            "vorname": leader.vorname,
            "nachname": leader.nachname,
            "role": leader.role,
            "gruppe": group.id,
            "standort": leader.location_id,
            "order": leader_order_value 
        }

        members_data = []
        for member in group.members:
            # hotfix for double object bug
            if member.id == leader.id:
                continue
            account_order = next((order for order in member.account_orders if order.group_order and order.group_order.date == selected_date), None)
            order_value = account_order.meal_id if account_order else 6

            members_data.append({
                "id": member.id,
                "vorname": member.vorname,
                "nachname": member.nachname,
                "role": member.role,
                "gruppe": group.id,
                "standort": member.location_id,
                "order": order_value
            })

        group_data = {
            "id": group.id,
            "name": group.name,
            "leader": leader_data,
            "members": members_data
        }

        result.append(group_data)

    return jsonify(result)

    #return jsonify([group.to_dict() for group in groups]), 200
    return jsonify(result), 200

def delete_group(request):
    data = request.get_json()
    group_id = data.get("group_id")
    group = Group.query.get(group_id)

    if not group:
        return {"error": "Group not found"}, 404 
    try:
        db.session.query(GroupLeader).filter_by(group_id=group_id).delete()
        db.session.query(GroupMembers).filter_by(group_id=group_id).delete()

        db.session.delete(group)
        db.session.commit()
        return {"success": "Group deleted successfully"}, 200
    except Exception as e:
        db.session.rollback()
        return {"error": f"Fehler beim LÃ¶schen der Gruppe: {str(e)}"}, 500

   
def change_group_name(group_id, request):
    data = request.get_json()
    group = Group.query.get(group_id)

    if not group:
        return {"error":"Group not found"}, 404

    new_name = data.get("name")
    if not name:
        return {"error": "Name muss angegeben werden"}, 400
    
    #group.leaders.append(leader)
    group.name = new_name
    db.session.commit()

    return {"success": "Name erfolgreich geändert"}, 200
    

def get_group_members(group_id):
    group = Group.query.get(group_id)
    if not group:
        return {"error":"Group not found"}, 404

    return jsonify([member.to_dict() for member in group.members]), 200

def get_group_leader(group_id):
    group = Group.query.get(group_id)

    if not group:
        return {"error":"Group not found"}, 404

    return jsonify([leader.to_dict() for leader in group.leaders]), 200

def set_group_leader(group_id, request):
    data = request.get_json()
    group = Group.query.get(group_id)

    if not group:
        return {"error":"Group not found"}, 404

    leader_id = data.get("leader_id")
    if not leader_id:
        return {"error": "Leader ID muss angegeben werden"}, 400
 

    leader = Account.query.get(leader_id)
    if not leader:
        return {"error": "Leader nicht gefunden"}, 404

    if leader in group.leaders:
        return {"error": "Account ist bereits Leader"}, 404
    
    group.leaders.insert(0, leader)
    db.session.commit()

    return {"success": "Leader erfolgreich gesetzt"}, 200

def remove_group_leader(group_id, request):
    data = request.get_json()
    group = Group.query.get(group_id)

    if not group:
        return {"error":"Group not found"}, 404

    leader_id = data.get("leader_id")
    if not leader_id:
        return {"error": "Leader ID muss angegeben werden"}, 400

    leader = Account.query.get(leader_id)
    if not leader:
        return {"error": "Leader nicht gefunden"}, 404
    
    if leader not in group.leaders:
        return {"error": "Account ist kein Leader der Gruppe"}, 404
    else:
        try:
            group.leaders.remove(leader)
            # hotfix remove also as member
            group.members.remove(leader)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return {"error": f"Fehler beim Entfernen des Leaders: {str(e)}"}, 500

    return {"success": "Leader erfolgreich entfernt"}, 200



def update_account_groups(account_id, request):
    
    """
    Aktualisiert die Gruppenmitgliedschaft eines Accounts.
    Erwartetes JSON-Format:
    {
        "add_groups": [group_id1, group_id2],  # Gruppen, zu denen das Mitglied hinzugefügt wird
        "remove_groups": [group_id3, group_id4] # Gruppen, aus denen das Mitglied entfernt wird
    }
    """

    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON data"}), 400

    add_groups = data.get("add_groups", [])
    remove_groups = data.get("remove_groups", [])

    account = Account.query.get(account_id)
    if not account:
        return jsonify({"error": "Account not found"}), 404

    # Gruppen abrufen, aus denen das Mitglied entfernt werden soll
    for group_id in remove_groups:
        group = Group.query.get(group_id)
        if group and account in group.members:
            group.members.remove(account)
        if group and account in group.leaders:
            group.leaders.remove(account)

    # Gruppen abrufen, zu denen das Mitglied hinzugefügt werden soll
    for group_id in add_groups:
        group = Group.query.get(group_id)
        if account.role == "group":
            if group and account not in group.leaders:
                group.leaders.insert(0, account)
        else:
            if group and account not in group.members:
                group.members.append(account)
    

    db.session.commit()

    return jsonify({"message": "Account groups updated successfully"}), 200


