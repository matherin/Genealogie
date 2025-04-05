from os import name
from flask import jsonify
from sqlalchemy import *
from ..datamodels import *
from ..database import db


# def get_wares(request):
#     wares = Ware.query.all()
#     return jsonify([user.to_dict() for user in users]), 200
