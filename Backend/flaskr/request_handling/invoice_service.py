from os import name
from flask import jsonify
from sqlalchemy import *
from sqlalchemy.orm import joinedload
from ..datamodels import *
from ..database import db
from datetime import datetime

def get_customer_contracts(request):

    return 