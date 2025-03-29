# from os import name
# from flask import jsonify
# from sqlalchemy import *
# from ..datamodels import *
# from ..database import db
# from ..utils.headers import check_headers
# from io import TextIOWrapper
# import csv
# import traceback 
# import sys
# from ..auth.password import generate_user_password, get_hash
# import re

# def split_name(name):
#     """
#     Hilfsmethode, um Vor- und Nachnamen aus einem Kürzel zu extrahieren.
#     Falls nur ein Wort vorhanden ist,
#     wird alles als Vorname gespeichert und der Nachname bleibt leer.
#     """
#     parts = re.findall(r'[A-Z][^A-Z]*', name)
    
#     if len(parts) >= 2:
#         return parts[0], "".join(parts[1:]).strip()  # Erster Teil = Vorname, Rest = Nachname
    
#     return name, "" 

# def clean_group_name(group_name):
#     '''
#     Hilfsmethode, um den Gruppen-Namen zu bereinigen
#     '''
#     return group_name.split(" - ")[0]  # Nimmt nur den Teil vor dem ersten " - "

# def handle_csv_import(request):
#     if 'file' not in request.files:
#         return {"error": "No file provided"}, 400

#     file = request.files['file']

#     if file.filename == '':
#         return {"error": "No selected file"}, 400

#     # Prüfen, ob die Datei leer ist (Lesen von 1 Byte reicht aus)
#     file_content = file.read(1)
#     if file_content == b"":
#         return {"error": "Empty file"}, 400
#     file.seek(0) 

#     try:
#         reader = csv.DictReader(TextIOWrapper(file, encoding='utf-8'), delimiter=';')

#         # Prüfen, ob `fieldnames` vorhanden sind
#         fieldnames = reader.fieldnames
#         if not fieldnames:
#             return {"error": "Invalid or empty CSV headers"}, 400

#         missing_columns = check_headers(fieldnames)
#         if missing_columns:
#             return {"error": f"Missing columns in CSV: {', '.join(missing_columns)}"}, 400

#         # Accounts für "Frau X" erstellen
#         # frau_x_account = Account.query.filter_by(vorname="Frau X").first()
#         # if not frau_x_account:
#             # frau_x_password = generate_user_password()  
#             # frau_x_account = Account(
#                 # vorname="Frau",
#                 # nachname="X",
#                 # role="group",
#                 # password=get_hash(frau_x_password)  
#             # )
#             # db.session.add(frau_x_account)

#         # herr_x_account = Account.query.filter_by(vorname="Herr X").first()
#         # if not herr_x_account:
#             # herr_x_password = generate_user_password()
#             # herr_x_account = Account(
#                 # vorname="Herr",
#                 # nachname="X",
#                 # role="group",
#                 # password=get_hash(herr_x_password)  
#             # )
#             # db.session.add(herr_x_account)

#         # frau_x_fraux_account = Account.query.filter_by(vorname="Frau X/Frau X").first()
#         # if not frau_x_fraux_account:
#             # frau_x_fraux_password = generate_user_password() 
#             # frau_x_fraux_account = Account(
#                 # vorname="Frau X",
#                 # nachname="Frau X",
#                 # role="group",
#                 # password=get_hash(frau_x_fraux_password)  
#             # )
#             # db.session.add(frau_x_fraux_account)

#         db.session.commit()

#         # CSV-Inhalte verarbeiten
#         objects = [] 

#         for row in reader:
#             id = int(row["Kunden-Nr."])
#             location_name = row["Bereich"]
#             group_id = int(row["Gruppe-Nr."])

#             # Standort prüfen und erstellen
#             account_location = Location.query.filter_by(name=location_name).first()
#             if not account_location:
#                 new_location = Location(name=location_name)
#                 db.session.add(new_location)
#                 db.session.flush()  
#                 account_location = new_location

#             # if row["Gruppen-Name 2"] == "Frau X":
#                 # group_leader = frau_x_account.id
#             # elif row["Gruppen-Name 2"] == "Frau X/Frau X":
#                 # group_leader = frau_x_fraux_account.id
#             # else:
#                 # group_leader = herr_x_account.id




#             # Grupe prüfen und erstellen
#             account_group = Group.query.filter_by(id=group_id).first()
#             if not account_group:
#                 new_group = Group(id=group_id, name=clean_group_name(row["Gruppen-Name 1"]), location=account_location)
#                 db.session.add(new_group)
#                 db.session.flush()  
#                 account_group = new_group
#             else:
#                 account_group.name = clean_group_name(account_group.name)

#             # get or create leader account
#             leader_vorname, leader_nachname = split_name(row["Gruppen-Name 2"])
#             group_leader_acc = Account.query.filter_by(vorname=leader_vorname, nachname = leader_nachname).first()
#             if group_leader_acc is None:
#                 # Passwort generieren und hashen
#                 password = generate_user_password() 
#                 password_hash = get_hash(password)  

#                 # Account erstellen und das Passwort-Hash speichern
#                 group_leader_acc = Account(
#                     vorname=leader_vorname, 
#                     nachname=leader_nachname, 
#                     role="group",
#                     location_id=account_location.id,
#                     password=password_hash  
#                 )
#                 db.session.add(group_leader_acc)
#                 db.session.commit()

#                 group_leader = GroupLeader(
#                     group_id=group_id,
#                     leader_id=group_leader_acc.id
#                 )
#                 db.session.add(group_leader)
#                 db.session.commit()

#                 group_member = GroupMembers(
#                     group_id=group_id,
#                     member_id=group_leader_acc.id
#                 )
#                 db.session.add(group_member)
#                 db.session.commit()





#             vorname, nachname = split_name(row["Kürzel"])
#             # check if user exists already
#             if not Account.query.filter_by(vorname=vorname, nachname=nachname).first():
#                 # Passwort generieren und hashen
#                 password = generate_user_password() 
#                 password_hash = get_hash(password)  

#                 # Account erstellen und das Passwort-Hash speichern
#                 account = Account(
#                     vorname=vorname, 
#                     nachname=nachname, 
#                     role="user",
#                     location_id=account_location.id,
#                     password=password_hash  
#                 )

#                 db.session.add(account)
#                 db.session.commit()

#                 group_member = GroupMembers(
#                     group_id=group_id,
#                     member_id=account.id
#                 )
#                 db.session.add(group_member)
#                 db.session.commit()

#         # Accounts speichern
#         db.session.add_all(objects)
#         db.session.commit()

#         return {"message": "CSV file uploaded successfully"}, 200

#     except Exception as e:
#         db.session.rollback()
#         print(f"Traceback: {traceback.format_exc()}")  
#         print(f"Error while processing CSV: {str(e)}")  # Debug
#         return {"error": f"Failed to process CSV file: {str(e)}"}, 500


# def account_exists(acc_id):
#     return Account.query.filter_by(id=acc_id).first() is not None

# def location_exists(loc_id):
#     return Location.query.filter_by(id=loc_id).first() is not None

# def get_location_by_id(loc_id):
#     return Location.query.filter_by(id=loc_id).first()

# def get_account_by_id(acc_id):
#     return Account.query.filter_by(id=acc_id).first()

# def group_exists(group_id):
#     return Group.query.filter_by(id=group_id).first() is not None

# def get_group_by_id(group_id):
#     return Group.query.filter_by(id=group_id).first()
