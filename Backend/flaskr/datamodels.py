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
            "role": self.role
        }
        if include_id:
            data["id"] = self.id
        return data
    
    def __repr__(self):
        return f"<User(id={self.id}, username={self.username}, role={self.role})>"

class DeliveryAddress(db.Model):
    __tablename__ = "delivery_address"
    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey("customer.id"), nullable=False)
    address_id = Column(Integer, ForeignKey("address.id"), nullable=False)

    address = relationship("Address")
    customer = relationship("Customer", back_populates="delivery_addresses")
    
    def to_dict(self):
        return self.address.to_dict()

class Address(db.Model):
    __tablename__ = "address"
    id = Column(Integer, primary_key=True)
    street = Column(String(255), nullable=False)
    house_number = Column(String(10), nullable=False)
    postal_code = Column(String(10), nullable=False)
    city = Column(String(100), nullable=True)
    country = Column(String(100), nullable=True)

    def to_dict(self):
        return {
            "street": self.street,
            "house_number": self.house_number,
            "postal_code": self.postal_code,
            "city": self.city,
            "country": self.country
        }

    def __repr__(self):
        return f"<Address(id={self.id}, street={self.street}, city={self.city})>"

class Customer(db.Model):
    __tablename__ = "customer"
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
    billing_address_id = Column(Integer, ForeignKey("address.id"), nullable=False)
    private = Column(Boolean)
    notes = Column(String)

    billing_address = relationship("Address", foreign_keys=[billing_address_id])
    delivery_addresses = relationship(
        "DeliveryAddress", back_populates="customer", cascade="all, delete-orphan"
    )


    def to_dict(self, include_id=True):
        data = {
            "id": self.id if include_id else None,
            "company": self.company,
            "account_number": self.account_number,
            "tax_number": self.tax_number,
            "contacts": [self.contact1, self.contact2, self.contact3],
            "phone_numbers": [self.phone1, self.phone2, self.phone3],
            "emails": [self.email1, self.email2, self.email3],
            "billing_address": self._address_to_dict(self.billing_address),
            "delivery_addresses": [da.to_dict() for da in self.delivery_addresses],
            "private": self.private,
            "notes": self.notes
        }
        return data

    def _address_to_dict(self, address):
        if address:
            return address.to_dict()
        return {}

    def __repr__(self):
        return f"<Customer(id={self.id}, firma={self.company})>"
    
class Good(db.Model):
    __tablename__ = "good"
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
            "description": self.description,
            "price": float(self.price) if self.price else None,
            "unit": self.unit,
            "waste_code": self.waste_code,
            "collection_group": self.collection_group,
            "category": self.category
        }
        if include_id:
            data["wid"] = self.id
        return data
    
    def __repr__(self):
        return f"<Good(id={self.id}, discription={self.description}, price={self.price})>"
    

class Contract(db.Model):
    __tablename__ = "contract"
    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey("customer.id"), nullable=False)
    date = Column(TIMESTAMP)
    input = Column(Boolean)

    customer = relationship("Customer")
    contract_goods = relationship("ContractGoods", back_populates="contract", lazy="joined")
    
    def to_dict(self, include_id=True):
        goods_list = [
        {
            "good": contract_good.good.to_dict(),
            "quantity": contract_good.quantity,
            "subtotal": float(contract_good.good.price) * contract_good.quantity
        } for contract_good in self.contract_goods
        ]
        print(goods_list)

        total_price = sum(item["subtotal"] for item in goods_list)

        data = {
            "customer": self.customer.to_dict(),
            "date": self.date.strftime("%d-%m-%Y") if self.date else None,
            "input": self.input,
            "goods": goods_list,
            "total_price": round(total_price, 2)
        }
        if include_id:
            data["vid"] = self.id
        return data
    
    def __repr__(self):
        return f"<Contract(id={self.id}, kunde_id={self.customer_id}, datum={self.date})>"


class ContractGoods(db.Model):
    __tablename__ = "contract_goods"
    contract_id = Column(Integer, ForeignKey("contract.id"), primary_key=True)
    good_id = Column(Integer, ForeignKey("good.id"), primary_key=True)
    quantity = Column(Integer, nullable=False)

    contract = relationship("Contract", back_populates="contract_goods")
    good = relationship("Good")

    def to_dict(self):
        return {
            "contract": self.contract.to_dict(),
            "good": self.good.to_dict(),
            "quantity": self.quantity
        }
    
    def __repr__(self):
        return f"<ContractGoods(contract_id={self.contract_id}, good_id={self.good_id}, quantity={self.quantity})>"