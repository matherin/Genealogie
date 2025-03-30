import os
from flask import Flask, request, make_response, jsonify
from flask_sqlalchemy import SQLAlchemy
from .database import db
from .routes import users_bp, wares_bp, contracts_bp, auth_bp, customers_bp
from .auth.jwt import validate_session
from dotenv import load_dotenv
from flasgger import Swagger
from flask_cors import CORS

# Load environment variables from .env file
load_dotenv()

def create_app(test_config=None):
    # Initialisierung der Flask-App und SQLAlchemy
    app = Flask(__name__)
    CORS(app, origins="*", methods=["PUT", "OPTIONS", "GET", "POST"], allow_headers=["Content-Type", "Authorization"])
    app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@database:5432/{os.getenv('POSTGRES_DB')}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize Swagger
    app.config['SWAGGER'] = {
        "title": "Metci API",
        "uiversion": 3
    }
    swagger = Swagger(app)

    @app.before_request
    def auth():
        cookie = request.cookies.get("Session")
        if not cookie:
            return
            
        if not validate_session(request.cookies.get("Session")):
            return make_response(jsonify({"error": "Unauthorized access"}), 403)


    @app.route('/')
    def home():
        return "Welcome to Metci!", 200
    
    # import der blueprints
    app.register_blueprint(users_bp)
    app.register_blueprint(customers_bp)
    app.register_blueprint(contracts_bp)
    app.register_blueprint(wares_bp)
    app.register_blueprint(auth_bp)

    db.init_app(app)

    # hier werden alle tabellen erstellt die wir in den modellen definiert haben also account und meal etc
    with app.app_context():
        db.create_all()

        from types import SimpleNamespace
        from .request_handling.users_service import create_user, get_users

        # Überprüfen, ob bereits Accounts existieren
        req = SimpleNamespace(get_json=lambda: {})
        accs, status = get_users(req)

        if not accs.json:  # Falls keine Benutzer vorhanden sind
            admin_data = {
                "username": "Admin",
                "password": "1234567",
                "role": "admin",
            }

            admin_request = SimpleNamespace(get_json=lambda: admin_data)
            create_user(admin_request)

    return app

