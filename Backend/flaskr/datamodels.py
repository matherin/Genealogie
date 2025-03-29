from email.policy import default
from click import group
from . import db
from sqlalchemy import *
from sqlalchemy.orm import relationship
from datetime import date

'''
Hier kommen alle Datenmodelle in eins rein, dass ist weniger umständlich vielleicht 
und ein bisschen übersichtlicher.

Die zu den Datenmodellen dazugehörigen Funktionen, die aber nur in 'routes.py' aufgerufen 
werden, sind in dem '/request_handling' Ordner unter der jeweiligen 'x_service.py' Datei.
'''

class Location(db.Model):
    __tablename__ = "locations"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    groups = relationship("Group", back_populates="location")
    accounts = db.relationship("Account", back_populates="location")

    def to_dict(self):
        return {
            "location_id": self.id,
            "name": self.name,
            "groups": [group.to_dict() for group in self.groups]
        }


class Group(db.Model):
    __tablename__ = "groups"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)

    location_id = Column(ForeignKey("locations.id"))
    location = relationship("Location", back_populates="groups")

    leaders = relationship("Account", secondary="group_leader", back_populates="led_groups_by_leader")
    members = relationship("Account", secondary="group_members")

    group_orders = relationship("GroupOrder", back_populates="group")


    def to_dict(self):

        leader_list = sorted(
                [{"account_id": leader.id, "vorname": leader.vorname, "nachname": leader.nachname} for leader in self.leaders],
                key = lambda x : x['account_id'], 
                reverse=True)

        member_list = [{"account_id": member.id, "vorname": member.vorname, "nachname": member.nachname} for member in self.members]

        # filter members
        # -> all members such that m.id not in leader.id
        member_list = [m for m in member_list if m['account_id'] not in {x['account_id'] for x in leader_list}]
        return {
            "group_id": self.id,
            "name": self.name,
            "leaders": leader_list,
            "members": member_list, 
            "location_id": self.location_id
        }
    
    def __repr__(self):
        return f"<Group(id={self.id}, name={self.name})>"
    


class Account(db.Model):
    __tablename__ = "accounts"

    id = db.Column(db.Integer, primary_key=True)
    vorname = db.Column(db.String(50), nullable=False)
    nachname = db.Column(db.String(50), nullable=False)

    password = db.Column(db.String(128), nullable=False)
    
    role = db.Column(db.String(20), nullable=False, default="standard_user")
    location_id = Column(Integer, ForeignKey("locations.id"))
    location = relationship("Location")

    group = relationship("Group", secondary="group_members")
    led_groups_by_leader = relationship("Group", secondary="group_leader", back_populates="leaders")

    account_orders = relationship("AccountOrder", back_populates="account")

    def to_dict(self):
        return {
            "account_id": self.id,
            "vorname": self.vorname,
            "nachname": self.nachname,
            "role": self.role,
            "groups": [
            {
                "group_id": group.id,
                "group_name": group.name,
                "location_name": group.location.name if group.location else None,
                "location_id": group.location_id if group.location else None,
            }
            for group in self.group
        ],
            # "location_id": self.location.id if self.location and not self.group else None
            "location_id": self.location_id
        }


    
    def __repr__(self):
        return f"<Account(id={self.id}, vorname={self.vorname}, nachname={self.nachname}, role={self.role})>"
    
class Meal(db.Model):
    __tablename__ = "meals"

    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Float, nullable=False)

    meal_orders = relationship("MealOrder", back_populates="meal")

    def to_dict(self):
        return {
            "meal_id": self.id,
            "price": self.price
        }


'''
Bestellungs Managment (Orders)
'''
# Standortbestellung
class LocationOrder(db.Model):
    __tablename__ = "location_orders"

    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False, default=date.today)
    content = relationship("MealOrder", back_populates="location_order")

    def to_dict(self):
        return {
            "id": self.id,
            "date": self.date,
            "content": [meal_order.to_dict() for meal_order in self.content]
        }

class MealOrder(db.Model):
    __tablename__ = "meal_orders"

    id = Column(Integer, primary_key=True)
    meal_id = Column(Integer, ForeignKey("meals.id"), nullable=False)
    meal = relationship("Meal", back_populates="meal_orders")
    count = Column(Integer, nullable=False)

    location_order_id = Column(Integer, ForeignKey("location_orders.id"))
    location_order = relationship("LocationOrder", back_populates="content")

    def to_dict(self):
        return {
            "meal_id": self.meal_id,
            "count": self.count
        }

# Gruppenbestellung
class GroupOrder(db.Model):
    __tablename__ = "group_orders"
    id = Column(Integer, primary_key=True)
    group_id = Column(Integer, ForeignKey('groups.id'))
    date = Column(Date, nullable=False) 
    group = relationship("Group", back_populates="group_orders")
    content = relationship("AccountOrder", back_populates="group_order")

    def to_dict(self):
        return {
            "order_id": self.id,
            "date": self.date, 
            "content": [person_order.to_dict() for person_order in self.content]
        }

    def __repr__(self):
        return f"<GroupOrder(id={self.id}, group_id={self.group_id}, date={self.date}, group={self.group}, content={self.content})"


class AccountOrder(db.Model):
    __tablename__ = "account_orders"

    id = Column(Integer, primary_key=True)
    
    account_id = Column(Integer, ForeignKey('accounts.id'), nullable=False)
    account = relationship("Account", back_populates="account_orders")

    meal_id = Column(Integer, nullable=False)
    valid = Column(Boolean, nullable=False, default=True)
    
    group_order_id = Column(Integer, ForeignKey("group_orders.id"))
    group_order = relationship("GroupOrder", back_populates="content")


    def to_dict(self):
        return {
            "order_id": self.id,
            "account_id": self.account_id,
            "valid": self.valid,
            "meal_id": self.meal_id,
            "group_order_id": self.group_order_id
        }

    def __repr__(self):  
        return f"<AccountOrder(id={self.id}, account_id={self.account_id}, meal_id={self.meal_id}, valid={self.valid}, group_order_id={self.group_order_id})>"


''' 
Linking Tables zum Verknüpfen von Gruppe mit Leader und Members oder Orders zu Account
'''
# Gruppen
class GroupMembers(db.Model):
    __tablename__ = "group_members"
    id = Column(Integer, primary_key=true)
    member_id = Column("member_id", Integer, ForeignKey("accounts.id"))
    group_id = Column("group_id", Integer, ForeignKey("groups.id"))

class GroupLeader(db.Model):
    __tablename__ = "group_leader"
    id = Column(Integer, primary_key=true)
    leader_id = Column("leader_id", Integer, ForeignKey("accounts.id"))
    group_id = Column("group_id", Integer, ForeignKey("groups.id"))
