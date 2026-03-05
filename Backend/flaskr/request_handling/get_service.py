from os import name
from flask import jsonify
from sqlalchemy import *
from ..datamodels import *
from ..database import db

def get_seventy(request):
    data = Seventy.query.all()
    return jsonify([line.to_dict() for line in data]), 200

def get_seventy_pob_count(request):
    results = (
        db.session.query(
            Seventy.placeOfBirth,
            func.count(Seventy.id)
        )
        .group_by(Seventy.placeOfBirth)
        .all()
    )

    return jsonify({
        location: count for location, count in results
    }), 200

def get_eighty(request):
    data = Eighty.query.all()
    return jsonify([line.to_dict() for line in data]), 200

def get_eighty_pob_count(request):

    # Person
    pob_results = (
        db.session.query(
            Eighty.placeOfBirth,
            func.count(Eighty.id)
        )
        .group_by(Eighty.placeOfBirth)
        .all()
    )

    # Father
    father_results = (
        db.session.query(
            Eighty.pobFather,
            func.count(Eighty.id)
        )
        .group_by(Eighty.pobFather)
        .all()
    )

    # Mother
    mother_results = (
        db.session.query(
            Eighty.pobMother,
            func.count(Eighty.id)
        )
        .group_by(Eighty.pobMother)
        .all()
    )

    return jsonify({
        "person": {loc: count for loc, count in pob_results},
        "father": {loc: count for loc, count in father_results},
        "mother": {loc: count for loc, count in mother_results}
    }), 200

def get_sixty(request):
    data = Sixty.query.all()
    return jsonify([line.to_dict() for line in data]), 200

def get_sixty_pob_count(request):
    results = (
        db.session.query(
            Sixty.placeOfBirth,
            func.count(Sixty.id)
        )
        .group_by(Sixty.placeOfBirth)
        .all()
    )

    return jsonify({
        location: count for location, count in results
    }), 200

def get_fifty(request):
    data = Fifty.query.all()
    return jsonify([line.to_dict() for line in data]), 200

def get_fifty_pob_count(request):
    results = (
        db.session.query(
            Fifty.placeOfBirth,
            func.count(Fifty.id)
        )
        .group_by(Fifty.placeOfBirth)
        .all()
    )

    return jsonify({
        location: count for location, count in results
    }), 200

# def get_good(id, request):
#     good = Good.query.filter_by(id=id).first()

#     if not good:
#         return {"error": "Good not found"}, 404 

#     return jsonify(good.to_dict()), 200
