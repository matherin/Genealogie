from os import name
from flask import jsonify
from sqlalchemy import *
from sqlalchemy.orm import joinedload
from ..datamodels import *
from ..database import db
from datetime import datetime

def create_customer(request):
    data = request.get_json()
    if not data:
        return {"error": "Customer data is missing."}, 400

    company = data.get("company", "").strip()
    account_number = data.get("account_number", "").strip()
    tax_number = data.get("tax_number", "").strip()

    contact_data = data.get("contacts", [])
    phone_data = data.get("phone_numbers", [])
    email_data = data.get("emails", [])

    if not contact_data or len(contact_data) > 3:
        return {"error": "Contacts must be provided and contain a maximum of 3 entries."}, 400
    if not phone_data or len(phone_data) > 3:
        return {"error": "Phone numbers must be provided and contain a maximum of 3 entries."}, 400
    if not email_data or len(email_data) > 3:
        return {"error": "Emails must be provided and contain a maximum of 3 entries."}, 400

    contact1 = contact_data[0].strip() if contact_data else None
    contact2 = contact_data[1].strip() if len(contact_data) > 1 else None
    contact3 = contact_data[2].strip() if len(contact_data) > 2 else None
    phone1 = phone_data[0].strip() if phone_data else None
    phone2 = phone_data[1].strip() if len(phone_data) > 1 else None
    phone3 = phone_data[2].strip() if len(phone_data) > 2 else None
    email1 = email_data[0].strip() if email_data else None
    email2 = email_data[1].strip() if len(email_data) > 1 else None
    email3 = email_data[2].strip() if len(email_data) > 2 else None

    private = data.get("private", False)
    notes = data.get("notes", "").strip() or None

    # Validate billing and delivery address data
    billing_address_data = data.get("billing_address")
    delivery_addresses_data = data.get("delivery_addresses")

    if not contact1 or not email1 or not billing_address_data or not delivery_addresses_data:
        return {"error": "Missing required fields (contact1, email1, billing_address, delivery_addresses)."}, 400

    def normalize_address(address_data):
        return {
            "street": address_data.get("street", "").strip(),
            "house_number": address_data.get("house_number", "").strip(),
            "postal_code": address_data.get("postal_code", "").strip(),
            "city": address_data.get("city", "").strip() or None,
            "country": address_data.get("country", "").strip() or None
        }

    # Create billing address
    billing_address_normalized = normalize_address(billing_address_data)
    billing_address = Address(**billing_address_normalized)
    db.session.add(billing_address)
    db.session.commit()

    # Create customer instance (billing address first)
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
        billing_address_id=billing_address.id,
        private=private,
        notes=notes
    )
    db.session.add(new_customer)
    db.session.flush()  # Get customer.id before committing

    # Create delivery addresses
    for address_data in delivery_addresses_data:
        normalized = normalize_address(address_data)

        if normalized == billing_address_normalized:
            address_instance = billing_address
        else:
            address_instance = Address(**normalized)
            db.session.add(address_instance)
            db.session.flush()

        delivery_address = DeliveryAddress(
            address=address_instance,
            customer=new_customer
        )
        db.session.add(delivery_address)

    db.session.commit()

    return {"success": "Customer created successfully", "id": new_customer.id}, 201

def delete_customer(customer_id):
    customer = Customer.query.get(customer_id)
    if not customer:
        return {"error": "Customer not found"}, 404

    # Adressen-IDs merken
    billing_address_id = customer.billing_address_id
    delivery_address_ids = [d.address_id for d in customer.delivery_addresses]

    # Customer löschen (cascaded DeliveryAddresses werden auch gelöscht)
    db.session.delete(customer)

    # Delivery-Adressen aufräumen
    for address_id in delivery_address_ids:
        still_used = DeliveryAddress.query.filter_by(address_id=address_id).first()
        if not still_used:
            Address.query.filter_by(id=address_id).delete()

    # Billing-Adresse aufräumen
    if billing_address_id:
        other_customer = Customer.query.filter_by(billing_address_id=billing_address_id).first()
        used_as_delivery = DeliveryAddress.query.filter_by(address_id=billing_address_id).first()
        if not other_customer and not used_as_delivery:
            Address.query.filter_by(id=billing_address_id).delete()

    db.session.commit()

    return {"success": "Customer deleted successfully"}, 200


def get_customers(request):
    customers = Customer.query.options(joinedload(Customer.delivery_addresses), joinedload(Customer.billing_address)).all()
    customers_list = [customer.to_dict() for customer in customers]
    return jsonify(customers_list), 200


def get_customer(id, request):
    customer = Customer.query.options(joinedload(Customer.delivery_addresses), joinedload(Customer.billing_address)).filter_by(id=id).first()

    if not customer:
        return {"error": "Customer not found"}, 404 

    return jsonify(customer.to_dict()), 200


def update_customer(customer_id, data):
    customer = Customer.query.get(customer_id)
    if not customer:
        return jsonify({"error": "Customer not found"}), 404

    # Update simple customer fields
    customer.company = data.get("company", customer.company)
    customer.account_number = data.get("account_number", customer.account_number)
    customer.tax_number = data.get("tax_number", customer.tax_number)
    customer.private = data.get("private", customer.private)
    customer.notes = data.get("notes", customer.notes)

    # Update contacts
    contacts = data.get("contacts")
    if contacts:
        if len(contacts) > 3:
            return jsonify({"error": "Contacts must contain a maximum of 3 entries."}), 400
        customer.contact1 = contacts[0] if len(contacts) > 0 else None
        customer.contact2 = contacts[1] if len(contacts) > 1 else None
        customer.contact3 = contacts[2] if len(contacts) > 2 else None

    # Update phones
    phones = data.get("phone_numbers")
    if phones:
        if len(phones) > 3:
            return jsonify({"error": "Phone numbers must contain a maximum of 3 entries."}), 400
        customer.phone1 = phones[0] if len(phones) > 0 else None
        customer.phone2 = phones[1] if len(phones) > 1 else None
        customer.phone3 = phones[2] if len(phones) > 2 else None

    # Update emails
    emails = data.get("emails")
    if emails:
        if len(emails) > 3:
            return jsonify({"error": "Emails must contain a maximum of 3 entries."}), 400
        customer.email1 = emails[0] if len(emails) > 0 else None
        customer.email2 = emails[1] if len(emails) > 1 else None
        customer.email3 = emails[2] if len(emails) > 2 else None

    # === Update Billing Address ===
    billing_data = data.get("billing_address")
    if billing_data:
        billing_address = customer.billing_address
        billing_address.street = billing_data.get("street", billing_address.street)
        billing_address.house_number = billing_data.get("house_number", billing_address.house_number)
        billing_address.postal_code = billing_data.get("postal_code", billing_address.postal_code)
        billing_address.city = billing_data.get("city", billing_address.city)
        billing_address.country = billing_data.get("country", billing_address.country)

    # === Update Delivery Addresses ===
    delivery_data_list = data.get("delivery_addresses")
    if delivery_data_list is not None:
        # Remove old delivery address links (but keep address records if used elsewhere)
        for delivery_link in customer.delivery_addresses:
            db.session.delete(delivery_link)
        db.session.commit()

        for delivery_data in delivery_data_list:
            # Normalize and check if this address already exists
            normalized = {
                "street": delivery_data.get("street", "").strip(),
                "house_number": delivery_data.get("house_number", "").strip(),
                "postal_code": delivery_data.get("postal_code", "").strip(),
                "city": delivery_data.get("city", "").strip(),
                "country": delivery_data.get("country", "").strip(),
            }

            # Try to find existing address
            existing_address = Address.query.filter_by(**normalized).first()
            if existing_address:
                address = existing_address
            else:
                address = Address(**normalized)
                db.session.add(address)
                db.session.commit()

            # Create new delivery address link
            new_delivery = DeliveryAddress(customer_id=customer.id, address_id=address.id)
            db.session.add(new_delivery)

    db.session.commit()
    return jsonify({"success": "Customer update successful"}), 200