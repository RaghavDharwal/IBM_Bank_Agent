# backend/app/__init__.py file
from flask import Flask
from flask_cors import CORS
from .config import Config
from .utils.csv_handler import initialize_csv_files

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Enable CORS
    CORS(app, supports_credentials=True)

    # Import and register blueprints
    from .routes.admin_routes import admin_bp
    from .routes.user_routes import user_bp
    from .routes.api_routes import api_bp

    app.register_blueprint(admin_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(api_bp)

    with app.app_context():
        # Initialize CSV files on startup
        # initialize_csv_files()
        initialize_csv_files(app.config)

    return app