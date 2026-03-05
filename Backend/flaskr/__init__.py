import os
from flask import Flask, request, make_response, jsonify
from flask_sqlalchemy import SQLAlchemy
from .database import db
from .routes import get_bp
from .seed_seventy import *
from .seed_eighty import *
from .seed_sixty import *
from .seed_fifty import *
from dotenv import load_dotenv
from flasgger import Swagger
from flask_cors import CORS

# Load environment variables from .env file
load_dotenv()

def create_app(test_config=None):
    # Initialisierung der Flask-App und SQLAlchemy
    app = Flask(__name__)
    CORS(app, origins="*", methods=["OPTIONS", "GET"], allow_headers=["Content-Type"])
    app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@database:5432/{os.getenv('POSTGRES_DB')}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize Swagger
    app.config['SWAGGER'] = {
        "title": "Genea API",
        "uiversion": 3
    }
    swagger = Swagger(app)


    @app.route('/')
    def home():
        return "Welcome to Genea!", 200
    
    # import der blueprints
    app.register_blueprint(get_bp)

    db.init_app(app)

    # hier werden alle tabellen erstellt die wir in den modellen definiert haben also account und meal etc
    with app.app_context():
        db.create_all()
        seed_seventy_database()
        seed_eighty_database()
        seed_sixty_database()
        seed_fifty_database()

    return app

