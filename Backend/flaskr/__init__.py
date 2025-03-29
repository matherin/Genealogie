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
        return "Welcome to MensaNow!", 200
    
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

        ## TEMPORARY DAS PASST SCHON 🤮
        from types import SimpleNamespace
        from .request_handling.accounts_service import create_account,  get_accounts

        # check if accouints are there already
        req = SimpleNamespace(get_json= lambda : data)
        accs,status = get_accounts(req)
        if len([x for x in accs.json if x['vorname']=='Dev']) == 0:
            # init test admin account to log
            # DevDev:MN1234 
            # QUICK AND DIRTY !!!!!
            data = {
                "vorname": "Dev",
                "nachname": "Dev",
                "password": "c5e827217051734e6a645c004d9c2d00096a90209429072f383836e915f3520dbcdf82501e888adf2b7e3301b89c46fd4ccc5e6bc59f5a8ced2e94e1a7a28a7d",
                "role": "admin", 
            }

            admin_request = SimpleNamespace(get_json=lambda : data)
            create_account(admin_request)

            data = {
                "vorname": "Locat",
                "nachname": "Ion",
                "password": "c5e827217051734e6a645c004d9c2d00096a90209429072f383836e915f3520dbcdf82501e888adf2b7e3301b89c46fd4ccc5e6bc59f5a8ced2e94e1a7a28a7d",
                "role": "location"
            }

            admin_request = SimpleNamespace(get_json=lambda : data)
            create_account(admin_request)


            data = {
                "vorname": "Group",
                "nachname": "Per",
                "password": "c5e827217051734e6a645c004d9c2d00096a90209429072f383836e915f3520dbcdf82501e888adf2b7e3301b89c46fd4ccc5e6bc59f5a8ced2e94e1a7a28a7d",
                "role": "group"
            }

            admin_request = SimpleNamespace(get_json=lambda : data)
            create_account(admin_request)

            data = {
                "vorname": "Max",
                "nachname": "Mustermann",
                "password": "c5e827217051734e6a645c004d9c2d00096a90209429072f383836e915f3520dbcdf82501e888adf2b7e3301b89c46fd4ccc5e6bc59f5a8ced2e94e1a7a28a7d",
                "role": "user"
            }

            admin_request = SimpleNamespace(get_json=lambda : data)
            create_account(admin_request)

    return app

