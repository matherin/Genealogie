from sqlalchemy import Column, Integer, String, Boolean, DECIMAL, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from . import db

class User(db.Model):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(255), nullable=False)
    role = Column(String(255))
    password = Column(String(255), nullable=False)

class Address(db.Model):
    __tablename__ = "adressen"
    id = Column(Integer, primary_key=True)
    street = Column(String(255), nullable=False)
    house_number = Column(String(10), nullable=False)
    postal_code = Column(String(10), nullable=False)
    city = Column(String(100), nullable=False)
    country = Column(String(100), nullable=False)

class Customer(db.Model):
    __tablename__ = "kunden"
    id = Column(Integer, primary_key=True)
    company = Column(String(255))
    account_number = Column(String(50))
    tax_number = Column(String(50))
    contact1 = Column(String(255), nullable=False)
    contact2 = Column(String(255))
    contact3 = Column(String(255))
    phone1 = Column(String(20))
    phone2 = Column(String(20))
    phone3 = Column(String(20))
    email1 = Column(String(255), nullable=False)
    email2 = Column(String(255))
    email3 = Column(String(255))
    delivery_address_id = Column(Integer, ForeignKey("adressen.id"), nullable=False)
    billing_address_id = Column(Integer, ForeignKey("adressen.id"), nullable=False)
    private = Column(Boolean)
    notes = Column(String)

    delivery_address = relationship("Address", foreign_keys=[delivery_address_id])
    billing_address = relationship("Address", foreign_keys=[billing_address_id])

class Contract(db.Model):
    __tablename__ = "vertraege"
    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey("kunden.id"), nullable=False)
    date = Column(TIMESTAMP)
    input = Column(Boolean)

    customer = relationship("Customer")

class Goods(db.Model):
    __tablename__ = "waren"
    id = Column(Integer, primary_key=True)
    description = Column(String(255))
    price = Column(DECIMAL(10,2))
    unit = Column(String(50))
    waste_code = Column(String(250))
    collection_group = Column(String(250))
    category = Column(String(250))
    tax_class = Column(String(250))

class ContractGoods(db.Model):
    __tablename__ = "vertrag_waren"
    contract_id = Column(Integer, ForeignKey("vertraege.id"), primary_key=True)
    goods_id = Column(Integer, ForeignKey("waren.id"), primary_key=True)
    quantity = Column(Integer, nullable=False)

    contract = relationship("Contract")
    goods = relationship("Goods")
