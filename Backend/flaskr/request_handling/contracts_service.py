from os import name
from flask import jsonify
from sqlalchemy import *
from ..datamodels import *
from ..database import db
from sqlalchemy.orm import joinedload
from datetime import datetime

def create_contract(request):
    data = request.get_json()

    if not data:
        return {"error": "Contract data is missing."}, 400

    customer_id = data.get("customer_id")
    date_str = data.get("date")
    input_flag = data.get("input", False)
    goods = data.get("goods", [])  # List of dicts like {"good_id": 1, "quantity": 10}

    # Validate required fields
    if not customer_id or not date_str:
        return {"error": "Missing required fields (customer_id, date)."}, 400

    # Check if customer exists
    customer = Customer.query.get(customer_id)
    if not customer:
        return {"error": f"Customer with id {customer_id} does not exist."}, 404

    # Validate and parse date
    try:
        contract_date = datetime.strptime(date_str, "%d-%m-%Y")
    except ValueError:
        return {"error": "Date format should be DD-MM-YYYY."}, 400

    # Create contract
    new_contract = Contract(
        customer_id=customer_id,
        date=contract_date,
        input=input_flag
    )

    db.session.add(new_contract)
    db.session.commit()

    # Link goods to contract if provided
    for item in goods:
        good_id = item.get("good_id")
        quantity = item.get("quantity")

        if not good_id or not quantity:
            continue

        # Check if good exists
        good = Good.query.get(good_id)
        if not good:
            return {"error": f"Good with id {good_id} does not exist."}, 404

        contract_good = ContractGoods(
            contract_id=new_contract.id,
            good_id=good_id,
            quantity=quantity
        )
        db.session.add(contract_good)

    db.session.commit()

    return {"success": "Contract created successfully", "id": new_contract.id}, 201

def delete_contract(contract_id):
    contract = Contract.query.get(contract_id)
    print("Tried getting contract with ID", contract_id, "but got", contract, flush=True)

    if not contract:
        return {"error": "Contract not found"}, 404

    # Delete associated contract-goods entries
    contract_goods = ContractGoods.query.filter_by(contract_id=contract_id).all()
    for cg in contract_goods:
        db.session.delete(cg)

    # Delete the contract itself
    db.session.delete(contract)
    db.session.commit()

    return {"success": "Contract deleted successfully"}, 200

def get_contracts(request):
    contracts = Contract.query.options(
        joinedload(Contract.customer),
        joinedload(Contract.contract_goods).joinedload(ContractGoods.good)
    ).all()
    contracts_list = [contract.to_dict() for contract in contracts]
    return jsonify(contracts_list), 200


def get_contract(contract_id, request):
    contract = Contract.query.options(
        joinedload(Contract.customer),
        joinedload(Contract.contract_goods).joinedload(ContractGoods.good)
    ).filter_by(id=contract_id).first()

    if not contract:
        return {"error": "Contract not found"}, 404

    return jsonify(contract.to_dict()), 200


def update_contract(contract_id, data):
    contract = Contract.query.options(joinedload(Contract.customer)).get(contract_id)
    if not contract:
        return jsonify({"error": "Contract not found"}), 404

    # Update customer ID if provided
    if "customer_id" in data:
        customer = Customer.query.get(data["customer_id"])
        if not customer:
            return jsonify({"error": "Customer with the given ID not found"}), 400
        contract.customer_id = data["customer_id"]

    # Update date if provided
    if "date" in data:
        try:
            contract.date = datetime.strptime(data["date"], "%d-%m-%Y")
        except ValueError:
            return jsonify({"error": "Date format must be DD-MM-YYYY"}), 400

    # Update input/output flag
    if "input" in data:
        contract.input = data["input"]

    # Commit changes
    db.session.commit()
    return jsonify({"success": "Contract updated successfully"}), 200