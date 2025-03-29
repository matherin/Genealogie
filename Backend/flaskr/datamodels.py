from sqlalchemy import Column, Integer, String, Boolean, DECIMAL, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from . import db

class User(db.Model):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    username = Column(String(255), nullable=False)
    role = Column(String(255))
    password = Column(String(255), nullable=False)

    def to_dict(self, include_id=True):
        data = {
            "username": self.username,
            "role": self.role,
            "password": self.password
        }
        if include_id:
            data["id"] = self.id
        return data
    
    def __repr__(self):
        return f"<User(id={self.id}, username={self.username}, role={self.role})>"

class Address(db.Model):
    __tablename__ = "adressen"
    id = Column(Integer, primary_key=True)
    street = Column(String(255), nullable=False)
    house_number = Column(String(10), nullable=False)
    postal_code = Column(String(10), nullable=False)
    city = Column(String(100), nullable=False)
    country = Column(String(100), nullable=False)

    def to_dict(self):
        return {
            "straße": self.street,
            "hausnummer": int(self.house_number),
            "plz": self.postal_code,
            "stadt": self.city,
            "land": self.country
        }
    
    def __repr__(self):
        return f"<Address(id={self.id}, street={self.street}, city={self.city})>"

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

    def to_dict(self, include_id=True):
        data = {
            "firma": self.company,
            "kontonummer": self.account_number,
            "steuernummer": self.tax_number,
            "kontakte": [self.contact1, self.contact2, self.contact3],
            "telefonnummern": [self.phone1, self.phone2, self.phone3],
            "emails": [self.email1, self.email2, self.email3],
            "lieferadresse": self.delivery_address.to_dict() if self.delivery_address else None,
            "rechnungsadresse": self.billing_address.to_dict() if self.billing_address else None,
            "privat": self.private,
            "notizen": self.notes
        }
        if include_id:
            data["kid"] = self.id
        return data
    
    def __repr__(self):
        return f"<Customer(id={self.id}, firma={self.company})>"

class Contract(db.Model):
    __tablename__ = "vertraege"
    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey("kunden.id"), nullable=False)
    date = Column(TIMESTAMP)
    input = Column(Boolean)

    customer = relationship("Customer")

    def to_dict(self, include_id=True):
        data = {
            "kunde": self.customer.to_dict(),
            "datum": self.date.strftime("%d-%m-%Y") if self.date else None,
            "mwst": float(self.vat) if self.vat else None,
            "annahme": self.acceptance,
            "user": self.user.to_dict()
        }
        if include_id:
            data["vid"] = self.id
        return data
    
    def __repr__(self):
        return f"<Contract(id={self.id}, kunde_id={self.customer_id}, datum={self.date})>"

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

    def to_dict(self, include_id=True):
        data = {
            "bezeichnung": self.description,
            "preis": float(self.price) if self.price else None,
            "einheit": self.unit,
            "abfallschlüssel": self.waste_code,
            "sammelgruppe": self.collection_group,
            "kategorie": self.category
        }
        if include_id:
            data["wid"] = self.id
        return data
    
    def __repr__(self):
        return f"<Goods(id={self.id}, bezeichnung={self.description}, preis={self.price})>"

class ContractGoods(db.Model):
    __tablename__ = "vertrag_waren"
    contract_id = Column(Integer, ForeignKey("vertraege.id"), primary_key=True)
    goods_id = Column(Integer, ForeignKey("waren.id"), primary_key=True)
    quantity = Column(Integer, nullable=False)

    contract = relationship("Contract")
    goods = relationship("Goods")

    def to_dict(self):
        return {
            "vertrag": self.contract.to_dict(),
            "ware": self.goods.to_dict(),
            "menge": self.quantity
        }
    
    def __repr__(self):
        return f"<ContractGoods(vertrag_id={self.contract_id}, ware_id={self.goods_id}, menge={self.quantity})>"