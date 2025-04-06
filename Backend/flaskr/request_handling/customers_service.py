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

    # Check if contacts data exists and has the correct number of contacts (max 3)
    contact_data = data.get("contacts")
    if not contact_data or len(contact_data) > 3:
        return {"error": "Contacts must be provided and contain a maximum of 3 entries."}, 400
    contact1 = contact_data[0].strip() if contact_data[0] else None
    contact2 = contact_data[1].strip() if len(contact_data) > 1 else None
    contact3 = contact_data[2].strip() if len(contact_data) > 2 else None

    # Check if phone numbers data exists and has the correct number (max 3)
    phone_data = data.get("phone_numbers")
    if not phone_data or len(phone_data) > 3:
        return {"error": "Phone numbers must be provided and contain a maximum of 3 entries."}, 400
    phone1 = phone_data[0].strip() if phone_data[0] else None
    phone2 = phone_data[1].strip() if len(phone_data) > 1 else None
    phone3 = phone_data[2].strip() if len(phone_data) > 2 else None

    # Check if emails data exists and has the correct number (max 3)
    email_data = data.get("emails")
    if not email_data or len(email_data) > 3:
        return {"error": "Emails must be provided and contain a maximum of 3 entries."}, 400
    email1 = email_data[0].strip() if email_data[0] else None
    email2 = email_data[1].strip() if len(email_data) > 1 else None
    email3 = email_data[2].strip() if len(email_data) > 2 else None

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
    if "private" in data:
        customer.private = data["private"]
    if "notes" in data:
        customer.notes = data["notes"]

    # Validate and update emails
    if "emails" in data:
        email_data = data["emails"]
        if not email_data or len(email_data) > 3:
            return jsonify({"error": "Emails must be provided and contain a maximum of 3 entries."}), 400
        customer.email1 = email_data[0] if len(email_data) > 0 else None
        customer.email2 = email_data[1] if len(email_data) > 1 else None
        customer.email3 = email_data[2] if len(email_data) > 2 else None

    # Validate and update phone numbers
    if "phone_numbers" in data:
        phone_data = data["phone_numbers"]
        if not phone_data or len(phone_data) > 3:
            return jsonify({"error": "Phone numbers must be provided and contain a maximum of 3 entries."}), 400
        customer.phone1 = phone_data[0] if len(phone_data) > 0 else None
        customer.phone2 = phone_data[1] if len(phone_data) > 1 else None
        customer.phone3 = phone_data[2] if len(phone_data) > 2 else None
    
    # Validate and update contacts
    if "contacts" in data:
        contact_data = data["contacts"]
        if not contact_data or len(contact_data) > 3:
            return jsonify({"error": "Contacts must be provided and contain a maximum of 3 entries."}), 400
        customer.contact1 = contact_data[0] if len(contact_data) > 0 else None
        customer.contact2 = contact_data[1] if len(contact_data) > 1 else None
        customer.contact3 = contact_data[2] if len(contact_data) > 2 else None

    # Handle address updates (separate delivery and billing addresses)
    if "delivery_address" in data:
        delivery_data = data["delivery_address"]
        delivery_address = Address.query.get(customer.delivery_address_id)
        if not delivery_address:
            return jsonify({"error": "Delivery address not found"}), 404
        
        # Check if the delivery and billing address are the same
        if customer.delivery_address_id == customer.billing_address_id:
            # If they're the same, create a new address for billing if one is updated
            if "billing_address" in data:
                billing_data = data["billing_address"]
                new_billing_address = Address(
                    street=billing_data.get("street", delivery_address.street),
                    house_number=billing_data.get("house_number", delivery_address.house_number),
                    postal_code=billing_data.get("postal_code", delivery_address.postal_code),
                    city=billing_data.get("city", delivery_address.city),
                    country=billing_data.get("country", delivery_address.country)
                )
                db.session.add(new_billing_address)
                db.session.commit()  # Commit to get the new address ID
                
                # Now update the customer to link the new billing address
                customer.billing_address_id = new_billing_address.id
            # Update delivery address only if necessary
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
        else:
            # If addresses are different, update them separately
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
    
    # Update the billing address if provided and delivery/billing are not linked
    if "billing_address" in data and customer.delivery_address_id != customer.billing_address_id:
        billing_data = data["billing_address"]
        billing_address = Address.query.get(customer.billing_address_id)
        if not billing_address:
            return jsonify({"error": "Billing address not found"}), 404
        
        # Only update the billing address fields that are provided
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
