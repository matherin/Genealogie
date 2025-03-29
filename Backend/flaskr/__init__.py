from flask import Flask, request, make_response, jsonify
from flask_sqlalchemy import SQLAlchemy
from .database import db
from .routes import accounts_bp, group_bp, location_bp, additional_bp, auth_bp, invoice_bp, meal_bp
from .auth.jwt import validate_session
from dotenv import load_dotenv

from flask_cors import CORS

# Load environment variables from .env file
load_dotenv()

def create_app(test_config=None):
    # Initialisierung der Flask-App und SQLAlchemy
    app = Flask(__name__)
    CORS(app, origins="*", methods=["PUT", "OPTIONS", "GET", "POST"], allow_headers=["Content-Type", "Authorization"])
    app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://{os.getenv('POSTGRES_USER)}:{os.getenv('POSTGRES_PASSWORD)}@database:5432/{os.getenv('POSTGRES_DB')}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

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
    app.register_blueprint(accounts_bp)
    app.register_blueprint(group_bp)
    app.register_blueprint(location_bp)
    app.register_blueprint(additional_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(invoice_bp)
    app.register_blueprint(meal_bp)

    db.init_app(app)

    # hier werden alle tabellen erstellt die wir in den modellen definiert haben also account und meal etc
    with app.app_context():
        db.create_all()

        from types import SimpleNamespace
        from .request_handling.accounts_service import create_account, get_accounts

        # Überprüfen, ob bereits Accounts existieren
        req = SimpleNamespace(get_json=lambda: {})
        accs, status = get_accounts(req)

        if not accs.json:  # Falls keine Benutzer vorhanden sind
            admin_data = {
                "username": "Admin",
                "password": "1234567",
                "role": "admin",
            }

            admin_request = SimpleNamespace(get_json=lambda: admin_data)
            create_account(admin_request)

    return app

