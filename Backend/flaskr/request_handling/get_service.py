from os import name
from flask import jsonify
from sqlalchemy import *
from ..datamodels import *
from ..database import db

def get_seventy(request):
    data = Seventy.query.all()
    return jsonify([Seventy.to_dict() for line in data]), 200

# def get_good(id, request):
#     good = Good.query.filter_by(id=id).first()

#     if not good:
#         return {"error": "Good not found"}, 404 

#     return jsonify(good.to_dict()), 200
