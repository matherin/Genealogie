from os import name
from flask import jsonify
from sqlalchemy import *
from sqlalchemy.orm import joinedload
from ..datamodels import *
from ..database import db
from datetime import datetime

def create_customer(request):
    data = request.get_json()

    # Check if data is provided
    if not data:
        return {"error": "Customer data is missing."}, 400

    # Extract required fields
    company = data.get("company", "").strip()
    account_number = data.get("account_number", "").strip()
    tax_number = data.get("tax_number", "").strip()
    contact1 = data.get("contact1", "").strip()
    contact2 = data.get("contact2", "").strip() or None
    contact3 = data.get("contact3", "").strip() or None
    phone1 = data.get("phone1", "").strip() or None
    phone2 = data.get("phone2", "").strip() or None
    phone3 = data.get("phone3", "").strip() or None
    email1 = data.get("email1", "").strip()
    email2 = data.get("email2", "").strip() or None
    email3 = data.get("email3", "").strip() or None
    private = data.get("private", False)
    notes = data.get("notes", "").strip() or None

    # Extract and validate address data
    delivery_address_data = data.get("delivery_address")
    billing_address_data = data.get("billing_address")

    if not contact1 or not email1 or not delivery_address_data or not billing_address_data:
        return {"error": "Missing required fields (contact1, email1, delivery_address, billing_address)."}, 400

    # Normalize addresses to compare
    def normalize_address(address_data):
        return {
            "street": address_data.get("street", "").strip(),
            "house_number": address_data.get("house_number", "").strip(),
            "postal_code": address_data.get("postal_code", "").strip(),
            "city": address_data.get("city", "").strip() or None,
            "country": address_data.get("country", "").strip() or None
        }

    delivery_address_normalized = normalize_address(delivery_address_data)
    billing_address_normalized = normalize_address(billing_address_data)

    # Check if the addresses are the same
    if delivery_address_normalized == billing_address_normalized:
        delivery_address = Address(**delivery_address_normalized)
        db.session.add(delivery_address)
        db.session.commit()
        billing_address = delivery_address  # Reuse the same address
    else:
        delivery_address = Address(**delivery_address_normalized)
        billing_address = Address(**billing_address_normalized)

        db.session.add(delivery_address)
        db.session.add(billing_address)
        db.session.commit()

    # Create new customer instance
    new_customer = Customer(
        company=company,
        account_number=account_number,
        tax_number=tax_number,
        contact1=contact1,
        contact2=contact2,
        contact3=contact3,
        phone1=phone1,
        phone2=phone2,
        phone3=phone3,
        email1=email1,
        email2=email2,
        email3=email3,
        delivery_address_id=delivery_address.id,
        billing_address_id=billing_address.id,
        private=private,
        notes=notes
    )

    # Add to database and commit
    db.session.add(new_customer)
    db.session.commit()

    # Return success response
    return {"success": "Customer created successfully", "id": new_customer.id}, 201

def delete_customer(customer_id):
    customer = Customer.query.get(customer_id)
    print("Tried getting customer with ID", customer_id, "but got", customer, flush=True)

    if not customer:
        return {"error": "Customer not found"}, 404 

    # Retrieve and delete associated addresses
    delivery_address = Address.query.get(customer.delivery_address_id)
    billing_address = Address.query.get(customer.billing_address_id)

    if delivery_address:
        db.session.delete(delivery_address)
    if billing_address and billing_address.id != customer.delivery_address_id:
        db.session.delete(billing_address)

    # Delete customer after addresses
    db.session.delete(customer)
    db.session.commit()

    return {"success": "Customer deleted successfully"}, 200


def get_customers(request):
    customers = Customer.query.options(joinedload(Customer.delivery_address), joinedload(Customer.billing_address)).all()
    customers_list = [customer.to_dict() for customer in customers]
    return jsonify(customers_list), 200


def get_customer(id, request):
    customer = Customer.query.options(joinedload(Customer.delivery_address), joinedload(Customer.billing_address)).filter_by(id=id).first()

    if not customer:
        return {"error": "Customer not found"}, 404 

    return jsonify(customer.to_dict()), 200


def update_customer(customer_id, data):
    # Fetch the customer from the database by ID
    customer = Customer.query.get(customer_id)
    if not customer:
        return jsonify({"error": "Customer not found"}), 404
    
    # Update customer details
    if "company" in data:
        customer.company = data["company"]
    if "account_number" in data:
        customer.account_number = data["account_number"]
    if "tax_number" in data:
        customer.tax_number = data["tax_number"]
    if "contact1" in data:
        customer.contact1 = data["contact1"]
    if "contact2" in data:
        customer.contact2 = data["contact2"]
    if "contact3" in data:
        customer.contact3 = data["contact3"]
    if "phone1" in data:
        customer.phone1 = data["phone1"]
    if "phone2" in data:
        customer.phone2 = data["phone2"]
    if "phone3" in data:
        customer.phone3 = data["phone3"]
    if "email1" in data:
        customer.email1 = data["email1"]
    if "email2" in data:
        customer.email2 = data["email2"]
    if "email3" in data:
        customer.email3 = data["email3"]
    if "private" in data:
        customer.private = data["private"]
    if "notes" in data:
        customer.notes = data["notes"]

    # Update the delivery address if provided
    if "delivery_address" in data:
        delivery_data = data["delivery_address"]
        delivery_address = Address.query.get(customer.delivery_address_id)
        if not delivery_address:
            return jsonify({"error": "Delivery address not found"}), 404
        
        if "street" in delivery_data:
            delivery_address.street = delivery_data["street"]
        if "house_number" in delivery_data:
            delivery_address.house_number = delivery_data["house_number"]
        if "postal_code" in delivery_data:
            delivery_address.postal_code = delivery_data["postal_code"]
        if "city" in delivery_data:
            delivery_address.city = delivery_data["city"]
        if "country" in delivery_data:
            delivery_address.country = delivery_data["country"]

    # Update the billing address if provided
    if "billing_address" in data:
        billing_data = data["billing_address"]
        billing_address = Address.query.get(customer.billing_address_id)
        if not billing_address:
            return jsonify({"error": "Billing address not found"}), 404
        
        if "street" in billing_data:
            billing_address.street = billing_data["street"]
        if "house_number" in billing_data:
            billing_address.house_number = billing_data["house_number"]
        if "postal_code" in billing_data:
            billing_address.postal_code = billing_data["postal_code"]
        if "city" in billing_data:
            billing_address.city = billing_data["city"]
        if "country" in billing_data:
            billing_address.country = billing_data["country"]

    # Commit the changes to the database
    db.session.commit()

    return jsonify({"success": "Customer update successful"}), 200

# def get_location_name_by_id(location_id): 
#     location = Location.query.get(location_id)

#     if not location:    
#         return {"error": "Could not find location given by id"}, 400

#     return {"location_id": location.id, "name": location.name}, 200
